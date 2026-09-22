# coding: jif
temperature = 31
mood = "hangry"
message = "I have been waiting 3 weeks for my refund. This is unacceptable."

jif temperature > 30:
    print("it's hot")
else:
    print("it's not hot")

jif mood == "happy":
    print("serve coffee")
eljif mood == "hangry":
    print("serve snickers")
else:
    print("serve water")

jif message sounds like the customer is angry:
    print("escalate to a human")
else:
    print("let the chatbot handle it")
