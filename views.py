import datetime

from config import app, templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Depends, Form

from sqlalchemy.orm import Session

from db import get_db, Tour, User

# дані якого типу ми передаємо, бо серевер вважає що всі дані ми повертаємо у форматі json


@app.get('/', response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):  # параметр щоб дістати щось з бд
    tours = db.query(Tour).all()
    return templates.TemplateResponse('index.html', {'tours': tours, 'request': request})
    # сервер  повертає значення у форматі json


@app.post('/create-tour')
def create_tour(
    name: str = Form(),
    city: str = Form(),
    days: int = Form(),
    price: int = Form(),
    date: str = Form(),
    db: Session = Depends(get_db)
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