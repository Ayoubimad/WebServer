from REST.models import Vehicle, Alert, User, Contact


def create_users_and_vehicles():
    # Creazione degli utenti
    users = []
    for i in range(1, 4):
        username = f"admin{i}"
        password = username
        user = User.objects.create_user(username=username, password=password)
        contact = Contact.objects.create(phoneNumber='11111111111')
        user.contacts.add(contact)
        contact = Contact.objects.create(phoneNumber='22222222222')
        user.contacts.add(contact)
        users.append(user)
        print(f"User '{username}' created with password '{password}'")

    # Associazione di una macchina ad ogni utente
    for i, user in enumerate(users):
        vehicle = Vehicle.objects.create(id=i + 1, latitude=0, longitude=0, smoke=0, temperature=0)
        user.vehicles.add(vehicle)
        print(f"Vehicle {i + 1} associated with user '{user.username}'")
    vehicle = Vehicle.objects.get(pk=1)
    vehicle.latitude = 10
    vehicle.longitude = 10
    vehicle.save()


def create_alerts():
    # Coordinate di Modena
    modena_latitude = 44.647128
    modena_longitude = 10.925226

    # Creazione di alert per simulare la situazione
    for vehicle in Vehicle.objects.all():
        # Creazione di 3 alert per ogni veicolo
        for i in range(1, 4):
            # Se l'indice i è pari, posiziona l'alert entro il raggio di 5 km, altrimenti no
            if i % 2 == 0:
                # Coordinate per alert all'interno del raggio di 5 km
                alert_latitude = modena_latitude + 0.01 * i
                alert_longitude = modena_longitude - 0.01 * i
            else:
                # Coordinate per alert al di fuori del raggio di 5 km
                alert_latitude = modena_latitude + 0.1 * i
                alert_longitude = modena_longitude - 0.1 * i

            alert = Alert.objects.create(sender=vehicle, latitude=alert_latitude, longitude=alert_longitude,
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
    # create_alerts()
