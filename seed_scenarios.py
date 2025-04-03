import pandas as pd
from app import create_app, db
from app.models import Scenario

app = create_app()
app.app_context().push()

df = pd.read_csv('Rivals Aim Training - Scenarios.csv')

for index, row in df.iterrows():
    if pd.isna(row['Name']) or not str(row['Name']).strip():
        print(f"Skipping row {index} due to missing name.")
        continue

    scenario = Scenario(
        name=row['Name'],
        author=row.get('Author'),
        notes=row.get('Notes'),
        tags=row.get('Tags'),
        difficulty=row.get('Difficulty'),
        hero=row.get('Hero'),
        target=row.get('Target'),
        scoring=row.get('Scoring'),
        target_type=row.get('TargetType'),
        target_distance=row.get('TargetDistance'),
        target_range=row.get('TargetRange'),
        movement_type=row.get('MovementType'),
        movement_action=row.get('MovementAction'),
        movement_speed=row.get('MovementSpeed'),
        timer=row.get('Timer'),
        stay_behind_line=row.get('StayBehindLine'),
        use_abilities=row.get('UseAbilities'),
        no_ability_cooldown=row.get('NoAbilityCooldown'),
        scenario_code=row.get('ID')
    )
    db.session.add(scenario)

db.session.commit()
print("Scenarios imported successfully.")