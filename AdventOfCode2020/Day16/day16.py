import re

def check_nearby_tickets_error(tickets, ranges):
    error_rate = 0
    for t in tickets:
        for num in t:
            if len(check_valid_fields(num, ranges)) == 0:
                error_rate += num
                break
    return error_rate

def decode_fields(tickets, ranges):
    valid_tickets = []
    for t in tickets:
        fields = [check_valid_fields(num, ranges) for num in t]
        if len([f for f in fields if len(f) == 0]) == 0:
            valid_tickets.append(fields)
    intersections = [set.intersection(*map(set, [t[i] for t in valid_tickets])) for i in range(len(ranges))]
    fields = []
    for i, v in enumerate(intersections):
        if len(v) == 1: 
            fields.append(list(v)[0])
            continue
        options = v - set(fields)
        j = i + 1
        while j < len(intersections) and len(options) > 1:
            difference = options - intersections[j]
            if len(difference) > 0:
                options = difference
            j += 1
        fields.append(list(options)[0])
    return fields

def check_valid_fields(num, ranges):
    valid = []
    for k, v in ranges.items():
        if (num >= v[0] and num <= v[1]) or (num >= v[2] and num <= v[3]):
            valid.append(k)
    return valid

def test_input():
    test1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    ranges, mine, tickets = parse_input(test1)
    assert(check_nearby_tickets_error(tickets, ranges)) == 71

    test2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
    ranges, mine, tickets = parse_input(test2)
    assert(decode_fields(tickets, ranges)) == ["row", "class", "seat"]

def parse_input(input):
    rules, my_ticket, nearby = input.split("\n\n")
    ranges = {}
    for r in rules.splitlines():
        g = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", r)
        ranges[g.group(1)] = [int(i) for i in g.group(2, 3, 4, 5)]
    mine = [int(i) for i in my_ticket.splitlines()[-1].split(",")]
    tickets = [[int(i) for i in l.split(",")] for l in nearby.splitlines()[1:]]
    return ranges, mine, tickets

if __name__ == "__main__":
    test_input()
    with open("data.txt") as file:
        ranges, mine, tickets = parse_input(file.read())
        print(check_nearby_tickets_error(tickets, ranges))
        fields = list(decode_fields(tickets, ranges))
        product = 1
        for i, field in enumerate(fields):
            if field.startswith("departure"):
                product *= mine[i]
        print(product)