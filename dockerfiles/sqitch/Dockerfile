FROM sqitch/sqitch:v1.5.2

WORKDIR /sqitch

COPY dockerfiles/sqitch/sqitch-entrypoint.sh .
COPY backend/src/ocrchive/database/sqitch .

ENTRYPOINT ["/sqitch/sqitch-entrypoint.sh"]
