from REST.models import Vehicle, Alert, User


def create_users_and_vehicles():
    # Creazione degli utenti
    users = []
    for i in range(1, 4):
        username = f"admin{i}"
        password = username
        user = User.objects.create_user(username=username, password=password)
        users.append(user)
        print(f"User '{username}' created with password '{password}'")

    # Associazione di una macchina ad ogni utente
    for i, user in enumerate(users):
        vehicle = Vehicle.objects.create(id=i + 1, latitude=0, longitude=0, smoke=0, temperature=0)
        user.vehicles.add(vehicle)
        print(f"Vehicle {i + 1} associated with user '{user.username}'")


def create_alerts():
    # Coordinare Modena
    modena_latitude = 44.647128
    modena_longitude = 10.925226

    # Creazione di alert per simulare la situazione
    for vehicle in Vehicle.objects.all():
        # Creazione di 3 alert per ogni veicolo
        for i in range(1, 4):
            alert = Alert.objects.create(sender=vehicle, latitude=modena_latitude + i, longitude=modena_longitude - 1,
                                         smoke=vehicle.smoke, temperature=vehicle.temperature)
            # Associazione degli alert con tutti gli altri veicoli (tranne il mittente)
            for receiver_vehicle in Vehicle.objects.exclude(pk=vehicle.pk):
                alert.receivers.add(receiver_vehicle)
            print(f"Alert created for vehicle {vehicle.id}")


def script():
    User.objects.all().delete()
    Vehicle.objects.all().delete()
    Alert.objects.all().delete()
    create_users_and_vehicles()
    create_alerts()
