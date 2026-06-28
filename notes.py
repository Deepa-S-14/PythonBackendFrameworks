"""
Task 1 - Web Framework Foundations

Request-Response Cycle:
Browser -> URL Router -> View -> Model -> Database -> Response -> Browser

Middleware:
Middleware sits between the request and the view, and also between the response and the browser.

Built-in Middleware:
1. SecurityMiddleware - Adds security headers and protects against attacks.
2. SessionMiddleware - Manages user sessions.

WSGI vs ASGI:
WSGI:
- Handles synchronous requests.
- Default deployment interface for Django.

ASGI:
- Handles asynchronous requests.
- Used for WebSockets, chat apps, and real-time applications.

MVC vs MVT:
MVC:
Model -> Data
View -> User Interface
Controller -> Business Logic

Django MVT:
Model -> Model
View -> Controller
Template -> View
"""