from trycourier import Courier
#additional feature
def send_email(email,ans,auth):
                client = Courier(auth_token=auth)
                client.send_message(
                        message={
                          "to": {
                            "email": f"{email}",
                          },
                          "content": {
                            "title": f"Answer from Research-Buddy",
                            "body": f"Hey ! \n Check out the answer to your question below. \nDo not reply back to this email. \n\n {ans}\nRegards\nResearch Buddy",
                          },
                          "data": {"note": f"\nDo not reply back to this email. \n\n {ans}\nRegards,\nReseach Buddy",
                          },
                          "routing": {
                                "method": "single",
                                "channels": ["email"],
                            },
                        }
                      )
                return True
