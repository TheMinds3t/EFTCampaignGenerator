# map list
def map_list():
    return ["Woods","Factory","Customs","Reserve","Lighthouse","Shoreline","Interchange","The Lab"]

# trader list
def trader_list():
    return ["Prapor","Therapist","Fence","Skier","Peacekeeper","Mechanic","Ragman","Jaeger"]

# the relational graph between locations
def map_graph():
    return {
        "Woods": ["Lighthouse","Factory"],
        "Factory": ["Customs","Reserve","Woods", "The Lab"],
        "Customs": ["Factory", "Interchange"],
        "Reserve": ["Factory"],
        "Lighthouse": ["Woods","Shoreline"],
        "Shoreline": ["Lighthouse"],
        "Interchange": ["Customs"],
        "The Lab": ["Factory"] 
        }