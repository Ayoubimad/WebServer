# REST API

Implementazione di una piccola API REST offre funzionalità CRUD (Create, Read, Update, Delete) per gestire i dati dei veicoli nel sistema.

## Endpoint e operazioni supportate

### `/api/vehicles/`

- **GET**: Ottiene l'elenco completo dei veicoli.
- **POST**: Crea un nuovo veicolo.

### `/api/vehicles/<vehicle_id>/`

- **GET**: Ottiene i dettagli di un veicolo specifico.
- **PUT**: Aggiorna un veicolo esistente.
    json_fields = ['id', 'latitude', 'longitude', 'smoke', 'temperature']
- **DELETE**: Elimina un veicolo esistente.

### `/api/alerts/`

- **POST**: Crea un nuovo alert.
  json_fields = ['sende_id', 'latitude', 'longitude', 'smoke', 'temperature']

### `/api/contacts/<vehicle_id>`

**GET**: Ottiene i contatti associati al proprietario del veicolo.

## Utilizzo

Esempi di utilizzo con `curl` su sistemi Linux-like:

```bash
# Ottieni tutti i veicoli
curl -X GET http://<IP_ADDRESS>:<PORT>/api/vehicles/

# Ottieni un veicolo specifico
curl -X GET http://<IP_ADDRESS>:<PORT>/api/vehicles/<vehicle_id>/

# Crea un nuovo veicolo
curl -X POST -H "Content-Type: application/json" -d '{"id": <vehicle_id>, "latitude": <latitude>, "longitude": <longitude>, "smoke": <smoke> , "temperature": <temperature>}' http://<IP>:<PORT>/api/vehicles/

# Aggiorna un veicolo esistente, al veicolo <vehicle_id> assegna la nuova posizione
curl -X PUT -H "Content-Type: application/json" -d '{"id": <vehicle_id>, "latitude": <latitude>, "longitude": <longitude>, "smoke": <smoke> , "temperature": <temperature>}' http://<IP_ADDRESS>:<PORT>/api/vehicles/<vehicle_id>/

# Elimina un veicolo
curl -X DELETE http://<IP_ADDRESS>:<PORT>/api/vehicles/<vehicle_id>/
```



