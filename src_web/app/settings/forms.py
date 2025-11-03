from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class VKSettingsForm(FlaskForm):
    vk_api_id = StringField("VK API ID / Access Token", validators=[DataRequired(), Length(min=10, max=512)])
    vk_group_id = StringField("VK Group ID (число, без минуса)", validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField("Сохранить")



