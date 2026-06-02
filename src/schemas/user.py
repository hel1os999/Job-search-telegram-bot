from pydantic import BaseModel, Field


class UserProfileDTO(BaseModel):
    skills: str | None = None
    experience: str | None = None
    desired_role: str | None = None
    desired_salary: int | None = None
    location: str | None = None

    def to_context(self) -> str:
        parts = []
        if self.desired_role:
            parts.append(f"Desired role: {self.desired_role}")
        if self.skills:
            parts.append(f"Skills: {self.skills}")
        if self.experience:
            parts.append(f"Experience: {self.experience}")
        if self.desired_salary:
            parts.append(f"Desired salary: {self.desired_salary}")
        if self.location:
            parts.append(f"Location: {self.location}")
        return "\n".join(parts) if parts else "No profile data"
