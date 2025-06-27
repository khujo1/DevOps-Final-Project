# Simulating an incident

## First check the running services:

>>docker ps
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS          PORTS                    NAMES
572c8805f3a4   frontend:latest           "python app.py"          20 minutes ago   Up 20 minutes   0.0.0.0:5000->5000/tcp   devops-final-project-frontend-1
69fc60c8eb20   backend:latest            "python app.py"          20 minutes ago   Up 20 minutes   0.0.0.0:5001->5001/tcp   devops-final-project-backend-1
99e8591277c0   prom/prometheus:v2.45.0   "/bin/prometheus --c…"   5 days ago       Up 20 minutes   0.0.0.0:9090->9090/tcp   devops-final-project-prometheus-1
16b86233534d   grafana/grafana:9.5.2     "/run.sh"                5 days ago       Up 20 minutes   0.0.0.0:3000->3000/tcp   devops-final-project-grafana-1

## I stop a frontend service:

>>docker stop 572c8
572c8

### Frontend is down 
![alt text](screenshots/image%20copy.png)

### Prometheus correctly identifies the service that is down
![alt text](screenshots/image%20copy%202.png)

### CPU resources that Frontend service was using decreased significantly
![alt text](screenshots/image%20copy%203.png)

