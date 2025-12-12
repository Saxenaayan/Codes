from app.database import org_collection, admin_collection, get_org_db
from app.utils.security import hash_password

class OrganizationService:

    @staticmethod
    def create_org(data):
        org_name = data.organization_name.lower()

        if org_collection.find_one({"organization_name": org_name}):
            return {"error": "Organization already exists"}, 400

        dynamic_name = f"org_{org_name}"

        admin_id = admin_collection.insert_one({
            "email": data.email,
            "password": hash_password(data.password),
            "organization": org_name
        }).inserted_id

        org_collection.insert_one({
            "organization_name": org_name,
            "collection_name": dynamic_name,
            "admin_id": admin_id
        })

        get_org_db(dynamic_name)

        return {"message": "Organization created",
                "organization": org_name,
                "collection": dynamic_name}, 201

    @staticmethod
    def get_org(org_name):
        org = org_collection.find_one({"organization_name": org_name})
        if not org:
            return {"error": "Organization not found"}, 404

        org["_id"] = str(org["_id"])
        org["admin_id"] = str(org["admin_id"])
        return org, 200

    @staticmethod
    def update_org(data):
        org_name = data.organization_name.lower()
        org = org_collection.find_one({"organization_name": org_name})

        if not org:
            return {"error": "Organization not found"}, 404

        new_collection = f"org_{org_name}"

        old_data = get_org_db(org["collection_name"]).find()
        new_db = get_org_db(new_collection)
        if old_data:
            new_db.insert_many(old_data)

        org_collection.update_one(
            {"organization_name": org_name},
            {"$set": {"collection_name": new_collection}}
        )

        return {"message": "Organization updated"}, 200

    @staticmethod
    def delete_org(org_name, admin_email):
        org = org_collection.find_one({"organization_name": org_name})
        if not org:
            return {"error": "Organization not found"}, 404

        admin = admin_collection.find_one({"email": admin_email})
        if admin["_id"] != org["admin_id"]:
            return {"error": "Unauthorized"}, 401

        get_org_db(org["collection_name"]).drop()
        org_collection.delete_one({"organization_name": org_name})

        return {"message": "Organization deleted"}, 200
