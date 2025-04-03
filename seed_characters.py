from app import create_app, db
from app.models import Character

app = create_app()
app.app_context().push()

characters = [
    "Adam Warlock", "Black Panther", "Black Widow", "Captain America", "Cloak & Dagger",
    "Doctor Strange", "Groot", "Hawkeye", "Hela", "Human Torch", "Hulk", "Invisible Woman",
    "Iron Fist", "Iron Man", "Jeff", "Loki", "Luna Snow", "Magik", "Magneto", "Mantis",
    "Mister Fantastic", "Moon Knight", "Namor", "Peni Parker", "Psylocke", "Rocket Raccoon",
    "Scarlet Witch", "Spider-Man", "Squirrel Girl", "Star-Lord", "Storm", "The Punisher",
    "The Thing", "Thor", "Venom", "Winter Soldier", "Wolverine"
]

for name in characters:
    if not Character.query.filter_by(name=name).first():
        db.session.add(Character(name=name))

db.session.commit()
print("✅ Characters seeded!")