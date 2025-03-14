import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

# Initialize FastAPI app
app = FastAPI(
    title="API Gateway",
    description="API Gateway for the Ride Sharing System",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
RIDER_SERVICE_URL = os.getenv("RIDER_SERVICE_URL", "http://rider-service:8002")
BOOKING_SERVICE_URL = os.getenv("BOOKING_SERVICE_URL", "http://booking-service:8003")
RIDE_MATCHING_SERVICE_URL = os.getenv("RIDE_MATCHING_SERVICE_URL", "http://ride-matching-service:8004")

# Service health route
@app.get("/health", tags=["health"])
async def health_check():
    async with httpx.AsyncClient() as client:
        try:
            health = {}
            # Check User Service
            user_response = await client.get(f"{USER_SERVICE_URL}/health")
            health["user_service"] = user_response.json()

            # Check Rider Service
            rider_response = await client.get(f"{RIDER_SERVICE_URL}/health")
            health["rider_service"] = rider_response.json()

            # Check Booking Service
            booking_response = await client.get(f"{BOOKING_SERVICE_URL}/health")
            health["booking_service"] = booking_response.json()

            # Check Ride Matching Service
            matching_response = await client.get(f"{RIDE_MATCHING_SERVICE_URL}/health")
            health["ride_matching_service"] = matching_response.json()

            return {"status": "healthy", "services": health}
        except httpx.HTTPError as e:
            return {"status": "unhealthy", "error": str(e)}

# User Service routes
@app.api_route("/users{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def user_service_proxy(request: Request, path: str):
    return await proxy_request(request, f"{USER_SERVICE_URL}/api/v1/users{path}")

@app.api_route("/token", methods=["POST"])
async def token_proxy(request: Request):
    return await proxy_request(request, f"{USER_SERVICE_URL}/api/v1/token")

# Rider Service routes
@app.api_route("/riders{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def rider_service_proxy(request: Request, path: str):
    return await proxy_request(request, f"{RIDER_SERVICE_URL}/api/v1/riders{path}")

@app.api_route("/distance-matrix", methods=["GET", "POST"])
async def distance_matrix_proxy(request: Request):
    return await proxy_request(request, f"{RIDER_SERVICE_URL}/api/v1/distance-matrix")

# Booking Service routes
@app.api_route("/rides{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def booking_service_proxy(request: Request, path: str):
    return await proxy_request(request, f"{BOOKING_SERVICE_URL}/api/v1/rides{path}")

# Proxy function to forward requests to appropriate service
async def proxy_request(request: Request, url: str):
    # Get request method and body
    method = request.method
    
    # Get query parameters
    params = dict(request.query_params)
    
    # Get headers (exclude host)
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    
    try:
        # Get request body if applicable
        body = None
        if method in ["POST", "PUT", "PATCH"]:
            body = await request.json()
        
        # Make request to service
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=body,
                timeout=30.0
            )
            
            # Return response from service
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)