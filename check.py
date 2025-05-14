from models.chat import ChatRelation
from models.user import User
from extensions import db
from models.job import Job

def check_chat_relation_integrity():
    errors = []

    all_users = {u.id for u in User.query.all()}
    all_jobs = {j.id for j in Job.query.all()}

    for relation in ChatRelation.query.all():
        if relation.user_id not in all_users:
            errors.append(f"[relation.id={relation.id}] user_id {relation.user_id} 不存在")
        if relation.buser_id not in all_users:
            errors.append(f"[relation.id={relation.id}] buser_id {relation.buser_id} 不存在")
        if relation.job_id not in all_jobs:
            errors.append(f"[relation.id={relation.id}] job_id {relation.job_id} 不存在")

    if errors:
        print("⚠️ 外键未连接上的数据：")
        for err in errors:
            print(err)
    else:
        print("✅ 所有 chat_relation 数据都连接正常。")

