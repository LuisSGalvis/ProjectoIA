from connect4.policy import Policy
from connect4.utils import find_importable_classes
from tournament import run_tournament, play

# Read all files within subfolder of "groups"
participants = find_importable_classes("groups", Policy)

# Build a participant list (name, class)
players = list(participants.items())

W=[]
a=0
# Run the tournament
for i in range(30):
    champion = run_tournament(
        players,
        play,  # You could also create your own play function for testing purposes
        shuffle=True,
    )
    w,x=champion
    W.append(w)
    if(w == 'Grupo X1'):
        a+=1

print("Champion:", W)
print(a)
