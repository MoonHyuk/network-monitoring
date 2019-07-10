# network-monitoring

주기적으로 TCP 통신이 가능한지 확인하고, 이상이 있다면 슬랙 알림을 보내줍니다.

## 사용 방법
```bash
> git clone git@gitlab.corp.sellmate.co.kr:sellmate/network-monitoring.git
> cd network-monitoring
> vi .env (.env.example과 아래 문서를 참고하여 .env를 만들어주세요)
> docker-compose build
> docker-compose up -d
```

### .env 변수들
- hosts: 모니터링 하고 싶은 서버의 ip 주소와 포트(ip:port 형식). 서버가 여러개일 경우 콤마(,)로 구분합니다. 포트가 명시되어 있지 않은 경우 기본적으로 80번 포트를 확인하게 됩니다.
- slack_token: slack bot의 토큰. `Apps > server-monitoring > settings`에서 이미 있는 봇의 토큰을 사용하거나 새롭게 만들어 사용해주세요.
- channel: 알림을 받을 채널 이름. 봇이 그 채널에 들어와있어야 합니다.

### troubleshooting
컨테이너를 띄우고 1분이 지났음에도 정상적으로 잘 작동되지 않는것 같으면
아래 명령어로 로그를 확인해보세요.
```bash
> docker exec -it network-monitoring sh
> cat /var/log/cron.log
```
