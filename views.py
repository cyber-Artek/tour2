import datetime
import logging

logging.basicConfig(level=logging.INFO)
from config import app, templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Depends, Form

from fastapi import Depends, HTTPException



from fastapi.responses import JSONResponse


from sqlalchemy.orm import Session

from db import get_db, Tour, User, Admin


from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# дані якого типу ми передаємо, бо серевер вважає що всі дані ми повертаємо у форматі json


@app.get('/', response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):  # параметр щоб дістати щось з бд
    tours = db.query(Tour).all()
    return templates.TemplateResponse('index.html', {'tours': tours, 'request': request})
    # сервер  повертає значення у форматі json

def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return user



def get_current_admin(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.user_id == user.id).first()
    if not admin:
        raise HTTPException(status_code=403, detail="Access denied. Admins only.")
    return admin

@app.post('/create-tour')
def create_tour(
    name: str = Form(),
    city: str = Form(),
    days: int = Form(),
    price: int = Form(),
    date: str = Form(),
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    tour = Tour(name=name, city=city, days=days, price=price, date=date)
    db.add(tour)
    db.commit()
    db.refresh(tour)
    return {'id': tour.id, 'name': tour.name, 'city': tour.city, 'days': tour.days, 'price': tour.price, 'date': tour.date.strftime('%Y-%m-%d')}

@app.get('/create-tour', response_class=HTMLResponse)
def create_tour_form(request: Request):
    return templates.TemplateResponse('create_tour.html', {"request": request})


@app.get('/register', response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse('register.html', {"request": request})


@app.post('/register', response_class=HTMLResponse)
def register(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    # Створюємо нового користувача
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Переадресація після успішної реєстрації
    return RedirectResponse(url="/success", status_code=303)


@app.get('/success', response_class=HTMLResponse)
def success(request: Request):
    return templates.TemplateResponse('success.html', {"request": request})





@app.post('/buy-tour', response_class=JSONResponse)
def buy_tour(
        tour_id: int = Form(...),
        db: Session = Depends(get_db)
):
    try:
        # Знаходимо тур
        tour = db.query(Tour).filter(Tour.id == tour_id).first()
        if not tour:
            logging.error('Tour not found: ID %s', tour_id)
            return {'status': 'error', 'message': 'Tour not found'}

        # Додаткова логіка покупки

        # Успішна покупка
        logging.info('Tour purchased: ID %s', tour_id)
        return {'status': 'success', 'message': 'Tour purchased successfully!'}

    except Exception as e:
        logging.error('Error during purchase: %s', str(e))
        return {'status': 'error', 'message': 'Server error'}




@app.get('/buy-tour', response_class=HTMLResponse)
def buy_tour_form(request: Request, db: Session = Depends(get_db)):
    tours = db.query(Tour).all()
    return templates.TemplateResponse('buy_tour.html', {'request': request, 'tours': tours})




@app.post('/edit-tour', response_class=JSONResponse)
def edit_tour(
    tour_id: int = Form(...),
    name: str = Form(...),
    city: str = Form(...),
    days: int = Form(...),
    price: int = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)

):
    try:
        # Знаходимо тур
        tour = db.query(Tour).filter(Tour.id == tour_id).first()
        if not tour:
            return {'status': 'error', 'message': 'Tour not found'}

        # Оновлюємо дані туру
        tour.name = name
        tour.city = city
        tour.days = days
        tour.price = price
        tour.date = datetime.datetime.strptime(date, '%Y-%m-%d')
        db.commit()
        db.refresh(tour)

        return {'status': 'success', 'message': 'Tour updated successfully!'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.post('/delete-tour', response_class=JSONResponse)
def delete_tour(tour_id: int = Form(...), db: Session = Depends(get_db),
                admin: Admin = Depends(get_current_admin)
                ):
    try:
        # Знаходимо тур
        tour = db.query(Tour).filter(Tour.id == tour_id).first()
        if not tour:
            return {'status': 'error', 'message': 'Tour not found'}

        # Видаляємо тур
        db.delete(tour)
        db.commit()

        return {'status': 'success', 'message': 'Tour deleted successfully!'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.get('/login', response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})


@app.post('/login', response_class=HTMLResponse)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Логіка для входу (наприклад, створення сесії)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_id", value=user.id)
    return response


@app.get('/logout', response_class=RedirectResponse)
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="user_id")
    return response



@app.get('/profile', response_class=HTMLResponse)
def profile(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@app.post('/make-admin', response_class=JSONResponse)
def make_admin(user_id: int = Form(...), db: Session = Depends(get_db)):
    # Перевіряємо, чи існує користувач
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {'status': 'error', 'message': 'User not found'}

    # Перевіряємо, чи користувач вже адміністратор
    existing_admin = db.query(Admin).filter(Admin.user_id == user_id).first()
    if existing_admin:
        return {'status': 'error', 'message': 'User is already an admin'}

    # Додаємо адміністратора
    admin = Admin(user_id=user_id)
    db.add(admin)
    db.commit()

    return {'status': 'success', 'message': f'User {user.username} is now an admin'}