from fastapi import FastAPI, Path, Query, Body, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

contacts = {1: { 
                "Name": "Strovosky",
                "Last name": "Peterson",
                "Company": "24/7",
                "Title": "Agent",
                "Mobile": 3023948119,
                "Landline": None,
                "Address": "Cll 78B # 34 - 21b",
                "Birthday": "07-11-1987",
                "Note": "He's gonna become the best programmer ever!"},
            2: {
                "Name": "Tawanda",
                "Last Name": "Peterson",
                "Company": "Exito",
                "Title": "Seller",
                "Mobile": 3228101401,
                "Landline": 5773538,  # This one should be prefixed with a 034
                "Address": "Cll 78B # 34 - 21b",
                "Birthday": "04-03-2001",
                "Note": "Devoted Mother"}}

# Models
class NewContact(BaseModel):
    name: str = Query(..., max_length=70)
    last_name: str = Query(..., max_length=70)
    company: Optional[str] = Query(None, max_length=70)
    title: Optional[str] = Query(None, max_length=70)
    mobile: int = Query(..., gt=1000000000)
    landline: Optional[int] = Query(None, gt=1000000)
    address: Optional[str] = Query(None, max_length=300)
    birthday: Optional[str] = Query(None, max_length=40)
    note: Optional[str] = Query(None, max_length=400)

class UpdateContacts(BaseModel):
    name: Optional[str] = Query(None, max_length=70)
    last_name: Optional[str] = Query(None, max_length=70)
    company: Optional[str] = Query(None, max_length=70)
    title: Optional[str] = Query(None, max_length=70)
    mobile: Optional[int] = Query(None, gt=1000000000)
    landline: Optional[int] = Query(None, gt=1000000)
    address: Optional[str] = Query(None, max_length=300)
    birthday: Optional[str] = Query(None, max_length=40)
    note: Optional[str] = Query(None, max_length=400)

# This will be the return of the home page.
@app.get("/")
def welcome():
    return """CONTACT MANAGER\nWelcome to CONTANCT MANAGER. This API will emulate your contact manager app in your mobile."""

# This Path Operation will display all the users created.
@app.get("/all_contacts")
def display_users():
    return contacts

# Here we'll pass a path parameter to find the contact.
@app.get("/find_contact/{field}")
def find_contact(field: str = Path(..., title="Contact Field", description="We'll identify the contact by using a piece of info from them.")):
    result = {}
    for contact in contacts:
        for cont in contacts[contact]:
            if field == str(contacts[contact][cont]):
                result.update(contacts[contact])
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Contact Not Found.")


@app.post("/contact/create")
def create_contact(new_contatct : NewContact = Body(...)):
    # Here we try to automatically check if there's a contact number missing and create the new contact on that missing number
    new_c = {}
    for ind, num_contact in enumerate(contacts, start=1):
        if ind != num_contact:
            new_c[ind] = {}
            new_c[ind]["Name"] = new_contatct.name
            new_c[ind]["Last Name"] = new_contatct.last_name
            new_c[ind]["Company"] = new_contatct.company
            new_c[ind]["Title"] = new_contatct.title
            new_c[ind]["Mobile"] = new_contatct.mobile
            new_c[ind]["Landline"] = new_contatct.landline
            new_c[ind]["Address"] = new_contatct.address
            new_c[ind]["Birthday"] = new_contatct.birthday
            new_c[ind]["Note"] = new_contatct.note
            return contacts.update(new_c)
    
    # If there's no number missing, we'll create the contact with the next number.
    ind = len(contacts) + 1
    contacts[ind] = {}
    contacts[ind]["Name"] = new_contatct.name
    contacts[ind]["Last Name"] = new_contatct.last_name
    contacts[ind]["Company"] = new_contatct.company
    contacts[ind]["Title"] = new_contatct.title
    contacts[ind]["Mobile"] = new_contatct.mobile
    contacts[ind]["Landline"] = new_contatct.landline
    contacts[ind]["Address"] = new_contatct.address
    contacts[ind]["Birthday"] = new_contatct.birthday
    contacts[ind]["Note"] = new_contatct.note
    return contacts

@app.put("/contact/update/{number}")
def update_contact(number: int = Path(..., ge=1000000000), updated_contact : UpdateContacts = Body(...)):
    for ind in contacts:
        if contacts[ind]["Mobile"] == number:
            if updated_contact.name != None:
                contacts[ind]["Name"] = updated_contact.name
            if updated_contact.last_name != None:
                contacts[ind]["Last Name"] = updated_contact.last_name
            if updated_contact.company != None:
                contacts[ind]["Company"] = updated_contact.company
            if updated_contact.title != None:
                contacts[ind]["Title"] = updated_contact.title
            if updated_contact.mobile != None:
                contacts[ind]["Mobile"] = updated_contact.mobile
            if updated_contact.landline != None:
                contacts[ind]["Landline"] = updated_contact.landline
            if updated_contact.address != None:
                contacts[ind]["Address"] = updated_contact.address
            if updated_contact.birthday != None:
                contacts[ind]["Birthday"] = updated_contact.birthday
            if updated_contact.note != None:
                contacts[ind]["Note"] = updated_contact.note
            return "Contact Updated."
    raise HTTPException(status_code=404, detail="Contact Not Found.")

@app.delete("/contact/delete/{number}")
def delete_contact(number : int = Path(..., ge=100000000)):
    ind_delete = 0
    for ind in contacts:
        if contacts[ind]["Mobile"] == number:
            ind_delete = ind
    del(contacts[ind_delete])
    return "Contact Deleted."
