# myservice-backend

# Example 소개

practice 에 있는 폴더별 예제에 대한 설명입니다.
|폴더명|특징| 
|--|--|
|step_1|기본적인 shorturl 생성 프로젝트|
|step_2|캐시가 도입된 shorturl 생성 프로젝트|
|step_3|캐시에 consistent hashing이 도입된 shorturl 생성 프로젝트|
|step_4|Queue와 비동기 worker가 도입된 shorturl 생성 프로젝트|
|step_6|db sharding 이 도입된 shorturl 생성 프로젝트|

# Test & Excute

실행을 위해서 docker 폴더의 docker compose 를 실행해야 합니다.
```c
cd docker
docker compose -f ./docker_compose.yaml up -d
