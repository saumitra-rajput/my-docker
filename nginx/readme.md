# Custom webpage on nginx docker container

## use dockerfile to build the image

Flag -t is used to name the image, (.) denotes the path where our dockerfile lives (which is current directory)
``` 
docker build -t nginx-web .
```

## use docker image to build the container
```
docker run -d -p 80:80 imagename
```

### Default path where nginx container html files lives

```
/usr/share/nginx/html
```

