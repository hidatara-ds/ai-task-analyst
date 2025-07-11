from sqlalchemy import TIMESTAMP, Boolean, Column, Float, Integer, String, Text

from db import Base


class EmbedUsers(Base):
    __tablename__ = "embed_users"
    session_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(TIMESTAMP)


class EmbedChats(Base):
    __tablename__ = "embed_chats"
    id = Column(Integer, primary_key=True)
    prompt = Column(Text)
    response = Column(Text)
    session_id = Column(Integer)
    include = Column(Boolean)
    connection_information = Column(Text)
    embed_id = Column(Integer)
    userId = Column(Integer)
    createdAt = Column(TIMESTAMP)


class EmbedConfigs(Base):
    __tablename__ = "embed_configs"
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    enabled = Column(Boolean)
    chat_mode = Column(Text)
    allowlist_domains = Column(Text)
    allow_model_override = Column(Boolean)
    allow_temperature_override = Column(Boolean)
    allow_prompt_override = Column(Boolean)
    max_chats_per_day = Column(Integer)
    max_chats_per_session = Column(Integer)
    workspace_id = Column(Integer)
    createdBy = Column(Integer)
    createdAt = Column(TIMESTAMP)


class Workspaces(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    slug = Column(Text)
    vectorTag = Column(Text)
    createdAt = Column(TIMESTAMP)
    openAiTemp = Column(Float)
    openAiHistory = Column(Integer)
    lastUpdatedAt = Column(TIMESTAMP)
    openAiPrompt = Column(Text)
    similarityThreshold = Column(Float)
    chatProvider = Column(Text)
    chatModel = Column(Text)
    topN = Column(Integer)
    chatMode = Column(Text)
    pfpFilename = Column(Text)
    agentProvider = Column(Text)
    agentModel = Column(Text)
    queryRefusalResponse = Column(Text)
