from datetime import datetime

from storage import Storage


class Note:
    def __init__(self, title: str, text: str, tags=None):
        self.title = title
        self.text = text
        self.tags = tags or []
        self.created_at = datetime.now()

    def __str__(self):
        tags = ", ".join(self.tags) if self.tags else "—"
        return (
            f"\n=== {self.title} ===\n"
            f"{self.text}\n"
            f"Tags: {tags}\n"
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        )


class NotesBook:
    FILENAME = "notes.pkl"

    def __init__(self):
        self.notes = Storage.load(self.FILENAME)

    def save(self):
        Storage.save(self.FILENAME, self.notes)

    # CREATE
    def add_note(self, title, text, tags):
        for note in self.notes:
            if note.title.lower() == title.lower():
                raise ValueError("Нотатка з таким заголовком вже існує")
        new_note = Note(title, text, tags)
        self.notes.append(new_note)
        self.save()
        return new_note

    # READ
    def list_notes(self):
        return self.notes

    def find_notes(self, keyword):
        keyword = keyword.lower()
        return [
            note for note in self.notes
            if keyword in note.title.lower()
            or keyword in note.text.lower()
            or any(keyword in tag.lower() for tag in note.tags)
        ]

    def find_by_title(self, title):
        for note in self.notes:
            if note.title.lower() == title.lower():
                return note
        return None

    # UPDATE
    def edit_note(self, title, new_text, new_tags):
        note = self.find_by_title(title)
        if not note:
            return False
        note.text = new_text
        note.tags = new_tags
        self.save()
        return True

    # DELETE
    def delete_note(self, title):
        note = self.find_by_title(title)
        if not note:
            return False
        self.notes.remove(note)
        self.save()
        return True

    # TAGS
    def get_all_tags(self):
        all_tags = set()
        for note in self.notes:
            all_tags.update(note.tags)
        return sorted(all_tags)

    def find_notes_by_tag(self, tag):
        tag = tag.lower()
        return [
            note for note in self.notes
            if any(tag == t.lower() for t in note.tags)
        ]
