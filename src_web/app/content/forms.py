from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    topic = StringField("Тема поста", validators=[DataRequired(), Length(min=5, max=200)])
    tone = StringField("Тональность", default="спокойный и вдохновляющий")
    generate_image = BooleanField("Generate Image", default=True)
    auto_post = BooleanField("Auto Post to VK", default=False)
    submit = SubmitField("Сгенерировать")

