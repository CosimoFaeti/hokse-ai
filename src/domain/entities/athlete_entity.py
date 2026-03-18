import datetime

from pydantic import BaseModel, Field


class Athlete(BaseModel):
    """ Represents an athlete"""

    id: int = Field(
        title="id", description="The id of the athlete"
    )

    username: str | None = Field(
        title="username", description="The username of the athlete"
    )

    resource_state: int = Field(
        title="resource_state", description="The state of the athlete"
    )

    first_name: str | None = Field(
        title="first_name", description="The first name of the athlete"
    )

    last_name: str | None = Field(
        title="last_name", description="The last name of the athlete"
    )

    bio: str | None = Field(
        title="bio", description="The biograph of the athlete"
    )

    city: str | None = Field(
        title="city", description="The city of the athlete"
    )

    state: str | None = Field(
        title="state", description="The state of the athlete"
    )

    country: str | None = Field(
        title="country", description="The country of the athlete"
    )

    sex: str | None = Field(
        title="sex", description="The gender of the athlete"
    )

    premium: bool | None = Field(
        title="premium", description="Whether the athlete is premium subscription"
    )

    summit: bool | None = Field(
        title="summit", description="Whether the athlete is summit subscription"
    )

    created_at: datetime | None = Field(
        title="created_at", description="The date and time the athlete was created"
    )

    updated_at: datetime | None = Field(
        title="updated_at", description="The date and time the athlete was updated"
    )

    badge_type: int | None = Field(
        title="badge_type", description="The badge type of the athlete"
    )

    weight: float | None = Field(
        title="weight", description="The weight of the athlete"
    )

    profile_medium: str | None = Field(
        title="profile_medium", description="The profile medium of the athlete"
    )

    profile: str | None = Field(
        title="profile", description="The profile name of the athlete"
    )

    friend: str | None = Field(
        title="friend", description="The friend of the athlete"
    )

    follower: str | None = Field(
        title="follower", description="The followed of the athlete"
    )
