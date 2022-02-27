from fastapi import FastAPI, Path


app = FastAPI()

contacts = {"Contact 1": { 
                "Name": "Strovosky",
                "Last name": "Peterson",
                "Company": "24/7",
                "Title": "Agent",
                "Mobile": 3023948119,
                "Lineline": None,
                "Address": "Cll 78B # 34 - 21b",
                "Birthday": "07-11-1987",
                "Note": "He's gonna become the best programmer ever!"},
            "Contact 2": {
                "Name": "Tawanda",
                "Peterson": "Peterson",
                "Company": "Exito",
                "Title": "Seller",
                "Mobile": 3228101401,
                "Lineline": 5773538,  # This one should be prefixed with a 034
                "Address": "Cll 78B # 34 - 21b",
                "Birthday": "04-03-2001",
                "Note": "Devoted Mother"}}

# Models


# This will be the return of the home page.
@app.get("/")
def welcome():
    return """CONTACT MANAGER\nWelcome to CONTANCT MANAGER. This API will emulate your contact manager app in your mobile."""

# This Path Operation will display all the users created.
@app.get("/all_contacts")
def display_users():
    return contacts

@app.get("/find_contact/{field}")
def find_contact(field: str = Path(..., title="Contact Field", description="We'll identify the contact by using a piece of info from them.")):
    for contact in contacts:
        for cont in contacts[contact]:
            if field == str(contacts[contact][cont]):
                return contacts[contact]
    return {"error: ": "Contact not found."}



