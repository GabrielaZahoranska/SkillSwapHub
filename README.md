# SkillSwap Hub

![SkillSwap Hub screenshot](docs/screenshot.png)

SkillSwap Hub is a Django app where signed-in users publish **skill listings** (title, category, long description). Anyone can browse listings and open a detail page to see the full text and the teacher’s username and email link. Only the person who created a listing can edit or delete it—session auth and view mixins enforce that.

I built it as a bootcamp-style MVP: full CRUD on one main model related to `User`, Postgres, class-based views, and templates (no separate front-end framework).

**Live app:** [add your deployed URL here](https://example.com)

## Technologies used

- Python 3.11  
- Django  
- PostgreSQL  
- psycopg2-binary (via Pipenv)  
- Django session authentication (login / logout / signup)  
- HTML templates + plain CSS (Flexbox + CSS Grid)
