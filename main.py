import schemas, utils, model
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Request
from database import Base,engine, getDB
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind = engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Which websites are allowed to call the API
    allow_credentials=True, # Whether to allow cookies/headers like Authorization
    allow_methods=["*"],    # Which HTTP methods are allowed (GET, POST, etc.)
    allow_headers=["*"],    # Which request headers are allowed
)
template = Jinja2Templates(directory="templates")

@app.get("/")
def homePage(request: Request):
    return template.TemplateResponse("index.html",{"request":request})

@app.post("/shorten")
def shortenURL(request: schemas.URLCreate, db : Session = Depends(getDB)):
    existingEntry = db.query(model.URL).filter(model.URL.long_url==request.longURL).first()
    if existingEntry:
        return {"short_url" : existingEntry.short_code, "long_url" : existingEntry.long_url}

    shortURL = utils.generateShortURl()
    urlEntry = model.URL(short_code = shortURL, long_url = request.longURL)
    db.add(urlEntry)
    db.commit()
    db.refresh(urlEntry)

    return {"short_url" : urlEntry.short_code, "long_url" : urlEntry.long_url}

@app.get("/analytics/{shortCode}")
def getAnalytics(shortCode:str, db:Session = Depends(getDB)):
    url_entry = db.query(model.URL).filter(model.URL.short_code== shortCode).first()
    if url_entry:
        return {"short_code" : url_entry.short_code
                ,"long_code" :url_entry.long_url
                ,"Clicks" :  url_entry.Clicks}
    
    else:
        return { "error": "404 not found"}

@app.get("/{short_code}")
def expandURL(short_code: str, db: Session = Depends(getDB)):
    url_entry = db.query(model.URL).filter(model.URL.short_code == short_code).first()

    if url_entry:
        url_entry.Clicks +=1
        db.commit()
        db.refresh(url_entry)
        return RedirectResponse(url=url_entry.long_url)
    else:
        return {"error": "Short URL not found"}