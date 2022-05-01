<%
    # Choose Pronoun
    if prefix:
        pronoun = "حضرتك"
    else:
        pronoun = "انتِ" if gender.value == "female" else "انت"

    tayeb = "طيبة" if gender.value == "female" else "طيب"

    if prefix:
        name = prefix + " " + first_name
    else:
        name = nickname if nickname else first_name
%>
كل سنه و ${pronoun} ${tayeb} يا ${name} ❤️ عيد اضحي مبارك عليكم جميعا 😀