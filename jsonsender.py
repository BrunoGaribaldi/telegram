import requests



def enviar():
    # URL de FlytBase
       # URL de FlytBase
    url = "https://api.flytbase.com/v2/integrations/webhook/6900081026671ac289bfd766"

    # Headers con tu token de autorización
    headers = {
        "Authorization": "Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmMzhlODM5NS1jMzFhLTRjZDMtOGIxNi0yNGJjNWY2MjVjN2MiLCJhdWQiOiIxOGRlNmVkYy05NGVmLTRiMGItYjA3ZS1iZjNjNTY5N2JhZGEiLCJzdWIiOiI2OGM0NGVhNzg4NzJmZDkxMzA1ZmEyOTUiLCJvaWQiOiI2OGM2MDIzMGRjMTVkNzk1MGZjN2NhNjIiLCJ1c2VyX3R5cGUiOjEsInVzZXJfaWQiOiI2ODcyOTRiOTY3NDJkOTk5NTcyMTZlOTgiLCJzY29wZXMiOltdLCJpYXQiOjE3NjE2MDk3NDQsImV4cCI6MTc2MTYxMDY0NH0.TKkfHYQHum2_SioT_DABvZmHVS_9kDH39rDZRe2DigOK02KJRG8pS0OCz-8dkRQSui40na5WO58KQrUQ1Pp42zmn6hEF-Loz-HvHS3cH916HxP2Zk5Nw2DcnRYDcqGswLOPS27chYnqcxLseoaWOt7QyoVAnvuN5hp_yxdnAMBnB23qqfpJx5hz9ekzmKeo8Y6nKycjqM-99SeH_RAp-q2ah0XxhJawWEIAZeZvONqNk1AY7cRn0Hxhju70XILxFqCyiB5GW0s3qAZh_0BMNd56XcjdwBl2KnG5V_Pu2x6qMtQdc-loF1gUZE1KgUbNRa-14Ys4mkPU0V0ZEEG_e2G3A80uPjep2y0XQk8QQMQCa8H_n0zL6xx_ZOu0nWgsE8nU4nybY_xfMvfXPLcGl9_1ua_8Nlf1YjD1aNsjhbDQ-hdzaFZMZt3oneRs5nZB-Phwj3SkOeZf6cQvaLykgAXTGYSD52hldn2tFqNuD84QgObNiNgN3ynwjmrugUXlsPPYKCmuYXW52AVCtZvEcQ8x3sLdoGuxBTi1txQdneNdgNFUCWTt-L53Bs6i6JfVevdyQ2tp98Yhj500akJt6WNEDV64YKVcacpZ-ocuwAMSJh_RcgkxKNBXEkH7FZHvtASGg3myNv95c2gLKOM08X9TTtX_Wu_y6vAI6WSkgOck",   # 👈 pegá tu token
        "Content-Type": "application/json"
    }

    # Tu JSON
    payload = {
        "timestamp": 1759445058883,
        "severity": 2,
        "description": "High temperature",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "altitude_msl": 100,
        "metadata": {
            "sensor_id": "TempSensor12A",
            "temperature": 50.2,
            "battery_level": 80
        }
    }
    # POST a FlytBase

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # <- esto hace tire excepción
    return response.json()   

    