from app.chat.conversation_store import ConversationStore
from app.database.models.conversation import ConversationModel
from app.database.models.message import MessageModel
from app.database.session import SessionLocal
from app.models.conversation import Conversation
from app.models.message import Message, Role
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class PostgresConversationStore(ConversationStore):
    def get(self, conversation_id: str) -> Conversation | None:
        with SessionLocal() as db:
            conversation_model = db.execute(
                select(ConversationModel)
                .where(ConversationModel.id == conversation_id)
                .options(selectinload(ConversationModel.messages))
            ).scalar_one_or_none()

            if conversation_model is None:
                return None

            conversation = Conversation()
            for message_model in conversation_model.messages:
                conversation.add_message(
                    Message(
                        role=Role(message_model.role), content=message_model.content
                    )
                )

            return conversation

    def save(self, conversation_id: str, conversation: Conversation) -> None:
        with SessionLocal() as db:
            conversation_model = db.get(ConversationModel, conversation_id)

            if conversation_model is None:
                conversation_model = ConversationModel(id=conversation_id)
                db.add(conversation_model)
                db.flush()

            existing_messages = (
                db.execute(
                    select(MessageModel)
                    .where(MessageModel.conversation_id == conversation_id)
                    .order_by(MessageModel.id)
                )
                .scalars()
                .all()
            )

            new_messages = conversation.messages[len(existing_messages) :]

            for message in new_messages:
                db.add(
                    MessageModel(
                        conversation_id=conversation_id,
                        role=message.role.value,
                        content=message.content,
                    )
                )

            db.commit()

    def get_conversations(self):
        with SessionLocal() as db:
            conversations = (
                db.execute(
                    select(ConversationModel).order_by(ConversationModel.updated_at.desc())
                )
                .scalars()
                .all()
            )

            return conversations
