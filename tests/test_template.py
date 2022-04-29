from socializer import services, models
from mako.template import Template


def test_gender_render():
    """To render genders in message, use `gender.value`"""
    contact = models.Contact(
        full_name="Test", first_name="Test", phone_num="", gender=models.Gender.FEMALE
    )
    template = Template(
        text="""
<%
result = "female" if gender.value == "female" else "male"
%>
${result}
    """
    )

    message = services.create_message(contact=contact, template=template)
    assert message.body.strip() == "female"