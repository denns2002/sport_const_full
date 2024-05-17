from profiles.models.profile import Profile


def appoint_trainer(boolean, user) -> None:
    trainer = Profile.objects.get(user=user)
    trainer.is_trainer = boolean
    trainer.save()
