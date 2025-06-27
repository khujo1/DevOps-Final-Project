## 🚨 Incident Simulation & Monitoring Validation

### Simulating a Service Failure

#### 1. Check Running Services

First, verify all services are running correctly:

```bash
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS          PORTS                    NAMES
572c8805f3a4   frontend:latest           "python app.py"          20 minutes ago   Up 20 minutes   0.0.0.0:5000->5000/tcp   devops-final-project-frontend-1
69fc60c8eb20   backend:latest            "python app.py"          20 minutes ago   Up 20 minutes   0.0.0.0:5001->5001/tcp   devops-final-project-backend-1
99e8591277c0   prom/prometheus:v2.45.0   "/bin/prometheus --c…"   5 days ago       Up 20 minutes   0.0.0.0:9090->9090/tcp   devops-final-project-prometheus-1
16b86233534d   grafana/grafana:9.5.2     "/run.sh"                5 days ago       Up 20 minutes   0.0.0.0:3000->3000/tcp   devops-final-project-grafana-1
```

#### 2. Simulate Frontend Service Failure

Stop the frontend service to simulate an incident:

```bash
docker stop <frontend-container-id>
# Example: docker stop 572c8
```

##### Frontend is down 
![alt text](screenshots/image%20copy.png)

##### Prometheus correctly identifies the service that is down
![alt text](screenshots/image%20copy%202.png)

##### CPU resources that Frontend service was using decreased significantly
![alt text](screenshots/image%20copy%203.png)


Currently this project doesn't contain mechanisms t detect such service failures, but it is important to note that 
alerting employees of such failures is a crucial part of system maintenance, and maybe i'll add that in the future as well :) 
But anyway here are some of them:

#### 4. Service Recovery

Restart the failed service:

```bash
docker start <frontend-container-id>
# My case: docker start 572c8
```

**Monitoring Recovery**:
- Prometheus targets show frontend as `UP` again
- Grafana dashboards resume displaying frontend metrics
- Application becomes accessible again
![alt text](screenshots/image%20copy%204.png)
![alt text](screenshots/image%20copy%205.png)
![alt text](screenshots/image%20copy%206.png)


### Key Observations

✅ **What Works Well**:
- Prometheus accurately detects service failures
- Grafana dashboards immediately reflect service status changes
- Metrics provide clear visibility into resource usage patterns
- Service discovery automatically updates target status

⚠️ **Areas for Future Improvement**:
- **Alerting**: Currently no automated notifications for service failures
- **Health Checks**: No proactive health monitoring beyond basic connectivity
- **Auto-Recovery**: No automatic restart mechanisms for failed services
- **Escalation**: No alert escalation or incident management integration

### Recommended Enhancements

For production environments, one could implement:

1. **Prometheus Alertmanager**:
```yaml
# Example alert rule
- alert: ServiceDown
  expr: up == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Service {{ $labels.instance }} is down"
```

2. **Docker Health Checks**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1
```

3. **Restart Policies**:
```yaml
services:
  frontend:
    restart: unless-stopped
```
