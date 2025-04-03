from app import create_app, db
from app.models import Scenario

app = create_app()
app.app_context().push()

# Find and update bad data
for s in Scenario.query.all():
    if isinstance(s.no_ability_cooldown, str):
        s.no_ability_cooldown = s.no_ability_cooldown == 'True'
    if isinstance(s.stay_behind_line, str):
        s.stay_behind_line = s.stay_behind_line == 'Yes'
    if isinstance(s.use_abilities, str):
        s.use_abilities = s.use_abilities == 'Yes'

db.session.commit()
print("✅ Cleaned up old scenario boolean fields.")