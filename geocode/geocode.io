Geocode := Object clone

Geocode reverse_geocode := method(lat, long,
    fp := URL with("http://maps.google.com/maps/geo?ll=" .. lat .. 
        "," .. long .. "&output=csv") fetch
    data := fp split(",")
    ret := Map clone
    ret atPut("status", data at(0))
    ret atPut("accuracy", data at(1))
    address := ""
    data slice(2) foreach(e, address = address .. e)
    ret atPut("address", address)
)

Geocode geocode := method(addr,
    addr = URL escapeString(addr)
    fp := URL with("http://maps.google.com/maps/geo?q=" .. addr .. 
        "&output=csv") fetch
    data := fp split(",")
    ret := Map clone
    ret atPut("status", data at(0))
    ret atPut("accuracy", data at(1))
    ret atPut("latitude", data at(2))
    ret atPut("longitude", data at(3))
)
