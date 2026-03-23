

## prerequisites to one cluster running

## run k8s commands to run the app 

- kubectl apply -f namespace.yml
- kubectl appy -f service.yml
- kubectl apply -f service.yml
- kubectl apply -f deployment.yml
- kubectl get all -n flask
- kubectl port-forward service/flask-service -n flask 8080:8080 --address=0.0.0.0  # sysport:podport(port mapping)


## clean up

- kubectl get all -n flask
- kubectl delete -f namespace.yml
- kubectl delete deployment/flask-deployment -n flask
- kubectl get all -n flask
- kubectl get all
