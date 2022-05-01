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

    emoji = "❤️" if prefix or gender.value == "male" else "😀"
%>
كل سنه و ${pronoun} ${tayeb} يا ${name} ${emoji} عيد مبارك عليكم جميعا 😀