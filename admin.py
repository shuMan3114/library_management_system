# stuff the admin can do --> view finances, add fines , check due dates , add books , plot : fianances , average borrow time , average revenue , etc etc.
from .modules.pasword import Password

class Admin:

    def __init__(self,admnID,f_name,l_name,contact):
        self.admnID = admnID
        self.f_name = f_name
        self.l_name = l_name
        self.contact = contact
        self.password = Password()
    
    
    
    
