import os, requests
from fastapi import status, HTTPException, Response

from schemas.hospital import CreateHospital, UpdateHospital
from dotenv import load_dotenv
from rabbitmq_utils import publish_event

load_dotenv()



def login(request):
    try:
        username = request.username
        password = request.password
        if not username and password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or password is missing.")

        response = requests.post(
            "http://0.0.0.0:8000/auth/users/login",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"}
        )

        return response.json()
    except Exception as ex:
        # print(ex)
        # print(f"Jara re{ex}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Internal Server Error")


def register(request):
    try:
        response = requests.post(
                f"http://0.0.0.0:8000/auth/users/register", json=request.model_dump()
            )
        if response.status_code == 200:
            print(response.json())
            return response.json()
        elif response.status_code == 400:
            response.status_code = status.HTTP_400_BAD_REQUEST

        else:
            return response.json()
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
    
def update_user(request, user_id: str, token: dict):
    try:
        response = requests.put(
                f"http://0.0.0.0:8000/auth/users/{user_id}", json={  
        "user_data": request, 
        "user_dict": token}
        )
        return response.json()
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get_user(user_id, user: dict):
    try:
        response = requests.get(
                f"http://0.0.0.0:8000/auth/users/{user_id}", json=user
            )
        print(response)
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get_all_users(user: dict):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    try:
        response = requests.get(
                f"http://0.0.0.0:8000/auth/users", json=user
            )
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_user(user: dict, user_id):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    try:
        response = requests.delete(
                f"http://0.0.0.0:8000/auth/users/{user_id}", json=user
            )
        if response.status_code == 200:
            pass
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Hospital operations

def create_hospital(data: dict, user: dict):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    try:
        details = {
            "hospital_data": data,
            "user_data": user
        }
        response = requests.post(
                f"http://0.0.0.0:8888/hospitals/create", json=details
            )
        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def update_hospital(data: dict, hospital_id: str, user: dict):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    try:
        details = {
            "hospital_data": data,
            "user_data": user,
            "hospital_id": hospital_id
        }
        response = requests.put(
                f"http://0.0.0.0:8888/hospitals", json=details
            )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def get_hospital(user: dict, hospital_id):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    try:
        details = {
            "hospital_id": hospital_id,
            "user_data": user
        }
        response = requests.get(
                f"http://0.0.0.0:8888/hospitals/{hospital_id}", json=details
            )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get_all_hospital(user: dict):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    try:
        response = requests.get(
                f"http://0.0.0.0:8888/hospitals", json=user
            )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def delete_hospital(user: dict, hospital_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    try:
        details = {
            "hospital_id": hospital_id,
            "user_data": user
        }
        response = requests.delete(
                f"http://0.0.0.0:8888/hospitals/{hospital_id}", json=details
            )
        if response.status_code == 204:
            return response
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detial=str(ex))
    

# Blood requests Operations starts here
def make_request(user: dict, req: dict):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    
    # get the user details
    response = requests.get(
            f"http://0.0.0.0:8000/auth/users/{user['user_id']}", json=user
        )
    if response.status_code == 200:
        res = response.json()
        # check if the user has a created hospital
        if not res.get('hospital_created'):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You need to have an hospital created first.")

    try:
        hospital_id = user.get('hospital_created')
        details = {
            "request": req,
            "user_data": user,
            "hospital_id": hospital_id
        }
        request_serv = requests.get(
            f"http://0.0.0.0:8000/requests/create", json=details
        )
        if request_serv.status_code != 201:
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{request_serv.status_code}")
        return "Request created successfully!"
        # elif not res['hospital_created']:
        #     return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You need to have an hospital created first.")
        # else:
        #     return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Hospital not created by the user.")
    except Exception as ex:
        print(f"From the exceptions: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))    

def get_request_single(user: dict, request_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    request_data = {
        "request_id": request_id,
        "user": user,
    }
    try:
        response = requests.get(
                f"http://0.0.0.0:8989/requests/{request_id}", json=request_data
            )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


def get_requests(user: dict, req_status):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    request_data = {
        "user": user,
        "status": req_status
    }
    try:
        response = requests.get(
                f"http://0.0.0.0:8989/requests", json=request_data
            )
        print(f"This is from the get request: {response}")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=str(response.json()["detail"]))
    except Exception as ex:
        # The ex.__dict__ is to get the actual error message from the exception
        res_dict = ex.__dict__
        raise HTTPException(status_code=res_dict["status_code"], detail=str(res_dict["detail"]))


def cancel_request(user: dict, request_id: str):
    request_data = {
        "request_id": request_id,
        "user": user,
    }
    try:
        response = requests.patch(
                f"http://0.0.0.0:8989/hospitals/{request_id}/cancel", json=request_data
            )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


def accept_request(user: dict, request_id: str):
    request_data = {
        "request_id": request_id,
        "user": user,
    }
    try:
        response = requests.patch(
                f"http://0.0.0.0:8989/hospitals/{request_id}/accept", json=request_data
            )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

# def check_
