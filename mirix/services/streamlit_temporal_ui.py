"""
Streamlit UI for Temporal Reasoning and Memory Decay Management

This module provides an interactive web interface for:
- Viewing memory statistics
- Configuring temporal reasoning settings
- Running memory decay tasks
- Visualizing memory health and decay patterns
- Chat interface with temporal reasoning
"""

import datetime as dt
import uuid
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone
from typing import Dict, List
from sqlalchemy import func

from mirix.log import get_logger
from mirix.services.memory_decay_task import memory_decay_task, MEMORY_TYPES
from mirix.services.temporal_reasoning_service import temporal_service
from mirix.services.chat_manager import chat_manager
from mirix.settings import temporal_settings
from mirix.schemas.chat_message import ChatMessageCreate
from mirix.schemas.user import User as PydanticUser

logger = get_logger(__name__)


class TemporalReasoningUI:
    """Streamlit UI for temporal reasoning management"""

    def __init__(self):
        """Initialize the UI"""
        st.set_page_config(
            page_title="MSLCA Temporal Reasoning",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def render(self):
        """Render the complete UI"""
        st.title("🧠 MSLCA Temporal Reasoning & Memory Decay")
        st.markdown("---")

        # Sidebar for configuration
        self.render_sidebar()

        # Main content tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "💬 Chat",
            "📊 Dashboard",
            "🔧 Settings",
            "🗑️ Memory Cleanup",
            "📈 Analytics",
            "🗄️ Database View"
        ])

        with tab1:
            self.render_chat()

        with tab2:
            self.render_dashboard()

        with tab3:
            self.render_settings()

        with tab4:
            self.render_cleanup()

        with tab5:
            self.render_analytics()
        
        with tab6:
            self.render_database_view()

    def render_sidebar(self):
        """Render the sidebar with connection info"""
        st.sidebar.title("🔌 Connection")

        # Lazy database connection - only initialize when trying to use database features
        if "session" not in st.session_state or st.session_state.session is None:
            if st.sidebar.button("🔗 Connect to Database"):
                # Trigger lazy connection
                if hasattr(st.session_state, 'get_db_session'):
                    st.session_state.get_db_session()
                    st.rerun()
            
            if st.session_state.get("session") is None:
                st.sidebar.warning("⚠️ Database not connected")
                st.sidebar.info("Click 'Connect to Database' button above, or work without database features.")
            
            st.session_state.org_id = st.sidebar.text_input(
                "Organization ID", 
                st.session_state.get("org_id", ""),
                help="Required for all database operations"
            )
            st.session_state.user_id = st.sidebar.text_input(
                "User ID", 
                st.session_state.get("user_id", ""),
                placeholder="e.g., user-d1850539",
                help="Enter your User ID to access YOUR memories. Use the same ID to return to your data."
            )
        else:
            st.sidebar.success("✓ Database connected")
            st.session_state.org_id = st.sidebar.text_input(
                "Organization ID", 
                st.session_state.get("org_id", ""),
                help="Required for all database operations"
            )
            st.session_state.user_id = st.sidebar.text_input(
                "User ID", 
                st.session_state.get("user_id", ""),
                placeholder="e.g., user-d1850539",
                help="Enter your User ID to access YOUR memories. Use the same ID to return to your data."
            )

        st.sidebar.markdown("---")

        # Temporal reasoning status
        st.sidebar.subheader("⚙️ System Status")
        if temporal_settings.enabled:
            st.sidebar.success("Temporal Reasoning: **ENABLED**")
        else:
            st.sidebar.error("Temporal Reasoning: **DISABLED**")

        st.sidebar.markdown(f"""
        **Current Settings:**
        - Rehearsal Threshold: `{temporal_settings.rehearsal_threshold}`
        - Deletion Threshold: `{temporal_settings.deletion_threshold}`
        - Max Age: `{temporal_settings.max_age_days}` days
        """)

        # Model selection section
        st.sidebar.markdown("---")
        st.sidebar.subheader("🤖 AI Model")
        
        # Initialize model in session state if not present
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = "gemini-2.0-flash"
        
        # Model provider filter
        model_provider = st.sidebar.selectbox(
            "Model Provider",
            ["Google Gemini", "AWS Bedrock", "OpenAI", "Anthropic"],
            index=0,
            help="Select the AI provider to use"
        )
        
        # Model selection based on provider
        if model_provider == "Google Gemini":
            available_models = [
                "gemini-2.0-flash",
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-1.5-pro",
                "gemini-2.0-flash-lite"
            ]
        elif model_provider == "AWS Bedrock":
            # AWS Bedrock requires inference profile ARNs, not model IDs
            # Check for custom ARN in environment, otherwise use default
            import os
            custom_arn = os.getenv("AWS_BEDROCK_MODEL_ARN")
            
            if custom_arn:
                # User has specified a custom inference profile ARN
                available_models = [custom_arn]
            else:
                # Default to common inference profile patterns
                # Users should set AWS_BEDROCK_MODEL_ARN in .env with their actual ARN
                available_models = [
                    "arn:aws:bedrock:us-east-1::inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                    "arn:aws:bedrock:us-east-1::inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0",
                ]
        elif model_provider == "OpenAI":
            available_models = [
                "gpt-5-nano",
                "gpt-4o-mini",
                "gpt-4o",
                "gpt-4.1-mini",
                "gpt-4.1"
            ]
        else:  # Anthropic
            available_models = [
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022"
            ]
        
        # Model selector
        selected_model = st.sidebar.selectbox(
            "Select Model",
            available_models,
            index=0 if st.session_state.selected_model not in available_models else available_models.index(st.session_state.selected_model),
            help="Choose which AI model to use for chat"
        )
        
        # Update session state if model changed
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.sidebar.success(f"✓ Model changed to: {selected_model}")
        
        # Show current model
        st.sidebar.info(f"**Current Model:** {st.session_state.selected_model}")

    def render_chat(self):
        """Render the chat interface"""
        st.header("💬 MSLCA Chat Assistant")

        # Chat works with or without database
        # Database is only needed for persistent storage
        db_available = st.session_state.get("session") is not None
        
        if not db_available:
            st.info("💡 Chat mode: Memory-only (messages not saved to database). Connect to database in sidebar for persistent storage.")

        # Initialize chat session
        if "chat_session_id" not in st.session_state:
            st.session_state.chat_session_id = str(uuid.uuid4())
            st.session_state.chat_history = []

        # Sidebar chat controls
        with st.sidebar:
            st.markdown("---")
            st.subheader("💬 Chat Controls")
            
            if st.button("🔄 New Conversation"):
                st.session_state.chat_session_id = str(uuid.uuid4())
                st.session_state.chat_history = []
                st.rerun()
            
            # Show session stats
            if st.session_state.chat_history:
                st.metric("Messages", len(st.session_state.chat_history))
                
            # Load previous sessions
            if st.button("📜 Load Previous Sessions"):
                self.show_previous_sessions()

        # Display chat messages
        st.subheader("Conversation")
        
        # Load existing messages from database
        if not st.session_state.chat_history:
            self.load_chat_history()

        # Chat container
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if msg.get("metadata"):
                        with st.expander("📊 Message Metadata"):
                            st.json(msg["metadata"])

        # Chat input
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            self.handle_chat_message(user_input)

        # Chat statistics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_importance = self.get_chat_avg_importance()
            st.metric("Avg Message Importance", f"{avg_importance:.2f}")
        
        with col2:
            temporal_health = self.get_chat_temporal_health()
            st.metric("Temporal Health", f"{temporal_health:.0%}")
        
        with col3:
            forgettable = self.get_chat_forgettable_count()
            st.metric("Forgettable Messages", forgettable)

    def load_chat_history(self):
        """Load chat history from database"""
        # Only load from database if connection is available
        if not st.session_state.get("session"):
            return  # Skip database loading, use in-memory only
            
        try:
            from mirix.server.server import db_context
            
            # Use the user-provided User ID from sidebar
            user_id = st.session_state.user_id
            org_id = st.session_state.org_id
            
            # Skip if no user ID provided
            if not user_id or user_id.strip() == "":
                return
            
            # Ensure organization and user exist in database
            user = self.ensure_org_and_user_exist(org_id, user_id)
            
            messages = chat_manager.get_session_messages(
                actor=user,
                session_id=st.session_state.chat_session_id,
                limit=100,
            )
            
            st.session_state.chat_history = [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "metadata": {
                        "id": msg.id,
                        "importance": msg.importance_score,
                        "access_count": msg.access_count,
                        "rehearsal_count": msg.rehearsal_count,
                    }
                }
                for msg in messages
            ]
            
        except Exception as e:
            logger.error(f"Error loading chat history: {e}")

    def ensure_org_and_user_exist(self, org_id: str, user_id: str) -> PydanticUser:
        """Ensure organization and user exist in database, create if not"""
        from mirix.services.organization_manager import OrganizationManager
        from mirix.services.user_manager import UserManager
        from mirix.schemas.organization import Organization as PydanticOrganization
        import hashlib
        
        org_manager = OrganizationManager()
        user_manager = UserManager()
        
        # Normalize org_id to match pattern ^org-[a-fA-F0-9]{8}
        if not org_id.startswith("org-"):
            # Create a valid org ID from user input using hash
            hash_input = org_id.encode('utf-8')
            hash_hex = hashlib.md5(hash_input).hexdigest()[:8]
            normalized_org_id = f"org-{hash_hex}"
        else:
            normalized_org_id = org_id
        
        # Check/create organization (managers handle their own sessions)
        try:
            org = org_manager.get_organization_by_id(normalized_org_id)
            if org is None:
                raise Exception("Organization not found")
        except:
            # Organization doesn't exist, create it with proper ID
            org = org_manager.create_organization(
                pydantic_org=PydanticOrganization(
                    id=normalized_org_id,
                    name=f"Organization {org_id}"
                )
            )
        
        # Check/create user
        try:
            user = user_manager.get_user_by_id(user_id)
            if user is None:
                raise Exception("User not found")
        except:
            # User doesn't exist, create it
            user = user_manager.create_user(
                pydantic_user=PydanticUser(
                    id=user_id,
                    name="Streamlit User",
                    timezone="UTC",
                    organization_id=org.id
                )
            )
        
        return user
    
    def handle_chat_message(self, user_input: str):
        """Handle a new chat message"""
        try:
            # Add user message to history (always in-memory)
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "metadata": {}
            })
            
            # Only store in database if connection is available
            if st.session_state.get("session"):
                try:
                    from mirix.server.server import db_context
                    
                    # Use the user-provided User ID from sidebar
                    user_id = st.session_state.user_id
                    org_id = st.session_state.org_id
                    
                    # Skip database storage if no user ID provided
                    if not user_id or user_id.strip() == "":
                        st.warning("⚠️ Please enter a User ID in the sidebar to save chat messages")
                        return
                    
                    # Ensure organization and user exist in database
                    user = self.ensure_org_and_user_exist(org_id, user_id)
                    
                    # Store user message in database
                    user_msg_data = ChatMessageCreate(
                        session_id=st.session_state.chat_session_id,
                        role="user",
                        content=user_input,
                        importance_score=0.7,
                        metadata_={
                            "source": "streamlit_ui",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                    
                    chat_manager.create_message(
                        actor=user,
                        message_data=user_msg_data,
                    )
                except Exception as db_err:
                    logger.warning(f"Failed to save to database: {db_err}")
            
            # Generate AI response
            assistant_response = self.generate_ai_response(user_input, st.session_state.chat_history)
            
            # Add assistant message to history (always in-memory)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": assistant_response,
                "metadata": {}
            })
            
            # Store assistant message in database if available
            if st.session_state.get("session"):
                try:
                    assistant_msg_data = ChatMessageCreate(
                        session_id=st.session_state.chat_session_id,
                        role="assistant",
                        content=assistant_response,
                        importance_score=0.6,
                        metadata_={
                            "source": "mirix_agent",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                    
                    chat_manager.create_message(
                        actor=user,
                        message_data=assistant_msg_data,
                    )
                except Exception as db_err:
                    logger.warning(f"Failed to save assistant response to database: {db_err}")
            
            # Rerun to show new messages
            st.rerun()
            
        except Exception as e:
            st.error(f"Error handling message: {e}")
            import traceback
            st.code(traceback.format_exc())

    def generate_ai_response(self, user_input: str, chat_history: list) -> str:
        """
        Generate AI response using the selected model
        
        Supports multiple providers: Gemini, AWS Bedrock, OpenAI, Anthropic
        """
        import os
        from mirix.settings import model_settings
        
        # Get selected model from session state
        selected_model = st.session_state.get("selected_model", "gemini-2.0-flash")
        
        # Build conversation context (last 10 messages)
        context_messages = chat_history[-10:]
        context = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in context_messages
        ])
        
        # Create prompt with system context
        system_context = """You are a helpful AI assistant integrated with MSLCA, a memory management system with temporal reasoning. 
All our conversations are stored with temporal decay - older, less important messages gradually fade. 
You can discuss temporal reasoning, memory decay, and general topics."""
        
        try:
            # Route to appropriate provider based on model name
            if selected_model.startswith("gemini-"):
                return self._generate_gemini_response(user_input, context, system_context)
            
            elif selected_model.startswith("anthropic.") or selected_model.startswith("arn:aws:bedrock:"):
                # Bedrock models: either model IDs (anthropic.*) or inference profile ARNs
                return self._generate_bedrock_response(selected_model, user_input, context, system_context)
            
            elif selected_model.startswith("gpt-"):
                return self._generate_openai_response(selected_model, user_input, context, system_context)
            
            elif selected_model.startswith("claude-"):
                return self._generate_anthropic_response(selected_model, user_input, context, system_context)
            
            else:
                return f"Error: Unknown model provider for '{selected_model}'"
                
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return self._fallback_response(user_input, chat_history, str(e))

    def _generate_gemini_response(self, user_input: str, context: str, system_context: str) -> str:
        """Generate response using Google Gemini"""
        try:
            import os
            import google.generativeai as genai
            
            # Get API key from environment
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return "Error: GEMINI_API_KEY not found in environment variables. Please set it in your .env file."
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Get selected model
            selected_model = st.session_state.get("selected_model", "gemini-2.0-flash")
            
            # Create model
            model = genai.GenerativeModel(selected_model)
            
            # Create full prompt
            full_prompt = f"{system_context}\n\nConversation history:\n{context}\n\nUser: {user_input}\n\nAssistant:"
            
            # Generate response
            response = model.generate_content(full_prompt)
            
            # Extract text
            if response and response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except ImportError:
            return "Error: google-generativeai package not installed. Install with: pip install google-generativeai"
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            raise

    def _generate_bedrock_response(self, model_id: str, user_input: str, context: str, system_context: str) -> str:
        """Generate response using AWS Bedrock"""
        try:
            import os
            from anthropic import AnthropicBedrock
            from mirix.settings import model_settings
            
            # Check AWS credentials - support both formats
            # Standard AWS format: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
            # MIRIX format: AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_REGION
            aws_access_key = model_settings.aws_access_key or os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_key = model_settings.aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
            aws_region = model_settings.aws_region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
            
            if not all([aws_access_key, aws_secret_key, aws_region]):
                missing = []
                if not aws_access_key:
                    missing.append("AWS_ACCESS_KEY_ID or AWS_ACCESS_KEY")
                if not aws_secret_key:
                    missing.append("AWS_SECRET_ACCESS_KEY")
                if not aws_region:
                    missing.append("AWS_REGION or AWS_DEFAULT_REGION")
                return f"Error: AWS credentials not configured. Missing: {', '.join(missing)}. Please set these in your .env file."
            
            # Create Bedrock client
            client = AnthropicBedrock(
                aws_access_key=aws_access_key,
                aws_secret_key=aws_secret_key,
                aws_region=aws_region,
            )
            
            # Create message
            message = client.messages.create(
                model=model_id,
                max_tokens=4096,
                system=system_context,
                messages=[
                    {"role": "user", "content": f"Conversation history:\n{context}\n\nUser: {user_input}"}
                ]
            )
            
            # Extract response
            if message.content and len(message.content) > 0:
                return message.content[0].text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except ImportError:
            return "Error: anthropic package not installed. Install with: pip install anthropic"
        except Exception as e:
            logger.error(f"Error generating Bedrock response: {e}")
            raise

    def _generate_openai_response(self, model_id: str, user_input: str, context: str, system_context: str) -> str:
        """Generate response using OpenAI"""
        try:
            from openai import OpenAI
            from mirix.settings import model_settings
            
            # Check API key
            if not model_settings.openai_api_key:
                return "Error: OPENAI_API_KEY not found in environment variables. Please set it in your .env file."
            
            # Create client
            client = OpenAI(api_key=model_settings.openai_api_key)
            
            # Create message
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": f"Conversation history:\n{context}\n\n{user_input}"}
                ],
                max_tokens=4096
            )
            
            # Extract response
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except ImportError:
            return "Error: openai package not installed. Install with: pip install openai"
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {e}")
            raise

    def _generate_anthropic_response(self, model_id: str, user_input: str, context: str, system_context: str) -> str:
        """Generate response using Anthropic API"""
        try:
            from anthropic import Anthropic
            from mirix.settings import model_settings
            
            # Check API key
            if not model_settings.anthropic_api_key:
                return "Error: ANTHROPIC_API_KEY not found in environment variables. Please set it in your .env file."
            
            # Create client
            client = Anthropic(api_key=model_settings.anthropic_api_key)
            
            # Create message
            message = client.messages.create(
                model=model_id,
                max_tokens=4096,
                system=system_context,
                messages=[
                    {"role": "user", "content": f"Conversation history:\n{context}\n\nUser: {user_input}"}
                ]
            )
            
            # Extract response
            if message.content and len(message.content) > 0:
                return message.content[0].text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except ImportError:
            return "Error: anthropic package not installed. Install with: pip install anthropic"
        except Exception as e:
            logger.error(f"Error generating Anthropic response: {e}")
            raise

    def _fallback_response(self, user_input: str, chat_history: list, error: str) -> str:
        """Generate fallback response when AI fails"""
        if "temporal" in user_input.lower() or "memory" in user_input.lower():
            return f"I understand you're asking about temporal reasoning and memory. In this system, all our conversations are stored with temporal decay - meaning older, less important messages will gradually fade. Your current chat session has {len(chat_history)} messages.\n\n(Note: AI model error - using fallback response)"
        elif "hello" in user_input.lower() or "hi" in user_input.lower():
            return f"Hello! I'm your MSLCA assistant. I can help you understand temporal reasoning, memory decay, and answer general questions. What would you like to know?\n\n(Note: AI model error - using fallback response)"
        else:
            return f"I received your message about '{user_input}'. (Note: AI model error - using fallback response)\n\nError details: {error}"

    def show_previous_sessions(self):
        """Show list of previous chat sessions"""
        try:
            # Use the user-provided User ID from sidebar
            user_id = st.session_state.user_id
            org_id = st.session_state.org_id
            
            # Skip if no user ID provided
            if not user_id or user_id.strip() == "":
                st.sidebar.info("ℹ️ Enter a User ID to view previous sessions")
                return
            
            # Ensure organization and user exist in database
            user = self.ensure_org_and_user_exist(org_id, user_id)
            
            sessions = chat_manager.list_sessions(actor=user, limit=20)
            
            if sessions:
                st.sidebar.markdown("### Previous Sessions")
                for session in sessions:
                    if st.sidebar.button(
                        f"📅 {session.last_message_at.strftime('%Y-%m-%d %H:%M')} ({session.message_count} msgs)",
                        key=f"session_{session.session_id}"
                    ):
                        st.session_state.chat_session_id = session.session_id
                        st.session_state.chat_history = []
                        st.rerun()
            else:
                st.sidebar.info("No previous sessions found")
                
        except Exception as e:
            st.sidebar.error(f"Error loading sessions: {e}")

    def get_chat_avg_importance(self) -> float:
        """Calculate average importance of chat messages"""
        try:
            from mirix.server.server import db_context
            from mirix.orm.chat_message import ChatMessage
            
            with db_context() as session:
                query = session.query(func.avg(ChatMessage.importance_score)).filter(
                    ChatMessage.session_id == st.session_state.chat_session_id
                )
                result = query.scalar()
                return float(result) if result else 0.5
                
        except Exception as e:
            logger.error(f"Error calculating avg importance: {e}")
            return 0.5

    def get_chat_temporal_health(self) -> float:
        """Calculate temporal health of chat messages"""
        try:
            from mirix.server.server import db_context
            from mirix.orm.chat_message import ChatMessage
            
            with db_context() as session:
                messages = session.query(ChatMessage).filter(
                    ChatMessage.session_id == st.session_state.chat_session_id
                ).all()
                
                if not messages:
                    return 1.0
                
                current_time = datetime.now(dt.timezone.utc)
                total_score = sum(
                    temporal_service.calculate_temporal_score(msg, current_time)
                    for msg in messages
                )
                
                return total_score / len(messages)
                
        except Exception as e:
            logger.error(f"Error calculating temporal health: {e}")
            return 0.5

    def get_chat_forgettable_count(self) -> int:
        """Count forgettable chat messages"""
        try:
            from mirix.server.server import db_context
            from mirix.orm.chat_message import ChatMessage
            
            with db_context() as session:
                messages = session.query(ChatMessage).filter(
                    ChatMessage.session_id == st.session_state.chat_session_id
                ).all()
                
                current_time = datetime.now(dt.timezone.utc)
                count = sum(
                    1 for msg in messages
                    if temporal_service.should_delete(msg, current_time)[0]
                )
                
                return count
                
        except Exception as e:
            logger.error(f"Error counting forgettable: {e}")
            return 0

    def render_dashboard(self):
        """Render the main dashboard"""
        st.header("📊 Memory Statistics Dashboard")

        if not st.session_state.get("org_id"):
            st.warning("⚠️ Please enter an Organization ID in the sidebar to view statistics.")
            return

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Memory Overview")
            self.render_memory_counts()

        with col2:
            st.subheader("Temporal Health")
            self.render_temporal_health()

        st.markdown("---")
        st.subheader("Memory Distribution by Type")
        self.render_memory_distribution()

    def render_memory_counts(self):
        """Render memory count cards"""
        if "session" not in st.session_state or not st.session_state.session:
            st.info("Connect database to view memory counts")
            return

        try:
            from mirix.server.server import db_context
            
            # Use a fresh session for queries
            with db_context() as session:
                org_id = st.session_state.org_id
                user_id = st.session_state.user_id or None

                counts = {}
                for memory_type in MEMORY_TYPES:
                    query = session.query(memory_type).filter(
                        memory_type.organization_id == org_id
                    )
                    if user_id:
                        query = query.filter(memory_type.user_id == user_id)
                    counts[memory_type.__name__] = query.count()

                # Display as metrics
                cols = st.columns(len(counts))
                for idx, (name, count) in enumerate(counts.items()):
                    with cols[idx]:
                        st.metric(label=name.replace("Memory", "").replace("Item", ""), value=count)

        except Exception as e:
            st.error(f"Error fetching memory counts: {e}")
            import traceback
            st.code(traceback.format_exc())

    def render_temporal_health(self):
        """Render temporal health indicators"""
        if "session" not in st.session_state or not st.session_state.session:
            st.info("Connect database to view temporal health")
            return

        try:
            from mirix.server.server import db_context
            
            # Use a fresh session for queries
            with db_context() as session:
                org_id = st.session_state.org_id
                user_id = st.session_state.user_id or None

                # Get decay statistics
                stats = memory_decay_task.get_decay_statistics(
                    session=session,
                    organization_id=org_id,
                    user_id=user_id,
                )

            total_forgettable = sum(
                s.get("total_forgettable", 0)
                for s in stats.values()
                if isinstance(s, dict)
            )

            # Display health metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    label="Forgettable Memories",
                    value=total_forgettable,
                    delta="Eligible for deletion",
                    delta_color="inverse"
                )

                with col2:
                    avg_importance = self.calculate_avg_importance(session, org_id, user_id)
                    st.metric(
                        label="Avg Importance",
                        value=f"{avg_importance:.2f}",
                        delta="Higher is better",
                        delta_color="normal"
                    )

                with col3:
                    avg_age = self.calculate_avg_age(session, org_id, user_id)
                    st.metric(
                        label="Avg Memory Age",
                        value=f"{avg_age:.0f} days",
                        delta="Across all types"
                    )

        except Exception as e:
            st.error(f"Error calculating temporal health: {e}")
            import traceback
            st.code(traceback.format_exc())

    def render_memory_distribution(self):
        """Render memory distribution chart"""
        if "session" not in st.session_state or not st.session_state.session:
            st.info("Connect database to view distribution")
            return

        try:
            from mirix.server.server import db_context
            
            # Use a fresh session for queries
            with db_context() as session:
                org_id = st.session_state.org_id
                user_id = st.session_state.user_id or None

                # Get importance distribution for each memory type
                data = []
                for memory_type in MEMORY_TYPES:
                    query = session.query(
                        memory_type.importance_score
                    ).filter(memory_type.organization_id == org_id)

                    if user_id:
                        query = query.filter(memory_type.user_id == user_id)

                    scores = [row[0] for row in query.all()]
                    for score in scores:
                        data.append({
                            "Type": memory_type.__name__.replace("Memory", "").replace("Item", ""),
                            "Importance Score": score
                        })

                if data:
                    df = pd.DataFrame(data)
                    fig = px.violin(
                        df,
                        x="Type",
                        y="Importance Score",
                        box=True,
                        points="outliers",
                        title="Importance Score Distribution by Memory Type"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No memory data available")

        except Exception as e:
            st.error(f"Error rendering distribution: {e}")
            import traceback
            st.code(traceback.format_exc())

    def render_settings(self):
        """Render settings configuration"""
        st.header("🔧 Temporal Reasoning Settings")

        st.markdown("""
        Configure how the temporal reasoning system behaves. Changes will affect:
        - Memory decay rates
        - Rehearsal thresholds
        - Deletion criteria
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Decay Parameters")

            new_lambda = st.slider(
                "Decay Lambda (λ)",
                min_value=0.01,
                max_value=0.2,
                value=float(temporal_settings.decay_lambda),
                step=0.01,
                help="Higher values = faster forgetting for low-importance memories"
            )

            new_alpha = st.slider(
                "Decay Alpha (α)",
                min_value=1.0,
                max_value=3.0,
                value=float(temporal_settings.decay_alpha),
                step=0.1,
                help="Controls long-term retention for high-importance memories"
            )

            new_max_age = st.number_input(
                "Max Age (days)",
                min_value=30,
                max_value=3650,
                value=temporal_settings.max_age_days,
                step=30,
                help="Hard delete memories older than this"
            )

        with col2:
            st.subheader("Thresholds")

            new_rehearsal = st.slider(
                "Rehearsal Threshold",
                min_value=0.0,
                max_value=1.0,
                value=float(temporal_settings.rehearsal_threshold),
                step=0.05,
                help="Relevance score needed to strengthen memories"
            )

            new_deletion = st.slider(
                "Deletion Threshold",
                min_value=0.0,
                max_value=0.5,
                value=float(temporal_settings.deletion_threshold),
                step=0.01,
                help="Temporal score below which memories are deleted"
            )

            new_boost = st.slider(
                "Rehearsal Boost",
                min_value=0.01,
                max_value=0.2,
                value=float(temporal_settings.rehearsal_boost),
                step=0.01,
                help="Importance increase per rehearsal"
            )

        st.markdown("---")

        st.subheader("Retrieval Weights")
        col1, col2 = st.columns(2)

        with col1:
            new_relevance_weight = st.slider(
                "Relevance Weight",
                min_value=0.0,
                max_value=1.0,
                value=float(temporal_settings.retrieval_weight_relevance),
                step=0.05,
                help="Weight for BM25/embedding score"
            )

        with col2:
            new_temporal_weight = st.slider(
                "Temporal Weight",
                min_value=0.0,
                max_value=1.0,
                value=float(temporal_settings.retrieval_weight_temporal),
                step=0.05,
                help="Weight for temporal score"
            )

        # Warning if weights don't sum to 1
        total_weight = new_relevance_weight + new_temporal_weight
        if abs(total_weight - 1.0) > 0.01:
            st.warning(f"⚠️ Weights sum to {total_weight:.2f}. Consider normalizing to 1.0")

        st.markdown("---")

        if st.button("💾 Save Settings", type="primary"):
            st.info("⚠️ Settings are read from environment variables or mirix/settings.py")
            st.markdown("""
            To persist these settings, update your configuration:

            **Environment Variables:**
            ```bash
            export MIRIX_TEMPORAL_DECAY_LAMBDA={:.2f}
            export MIRIX_TEMPORAL_DECAY_ALPHA={:.1f}
            export MIRIX_TEMPORAL_MAX_AGE_DAYS={}
            export MIRIX_TEMPORAL_REHEARSAL_THRESHOLD={:.2f}
            export MIRIX_TEMPORAL_DELETION_THRESHOLD={:.2f}
            export MIRIX_TEMPORAL_REHEARSAL_BOOST={:.2f}
            export MIRIX_TEMPORAL_RETRIEVAL_WEIGHT_RELEVANCE={:.2f}
            export MIRIX_TEMPORAL_RETRIEVAL_WEIGHT_TEMPORAL={:.2f}
            ```

            **Or edit `mirix/settings.py`** and restart the application.
            """.format(
                new_lambda,
                new_alpha,
                new_max_age,
                new_rehearsal,
                new_deletion,
                new_boost,
                new_relevance_weight,
                new_temporal_weight
            ))

    def render_cleanup(self):
        """Render memory cleanup interface"""
        st.header("🗑️ Memory Cleanup Manager")

        if not st.session_state.get("org_id"):
            st.warning("⚠️ Please enter an Organization ID in the sidebar.")
            return

        if "session" not in st.session_state or not st.session_state.session:
            st.error("❌ Database session required for cleanup operations")
            return

        st.markdown("""
        Identify and delete memories that have fallen below temporal relevance thresholds.
        """)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Preview Forgettable Memories")

            if st.button("🔍 Scan for Forgettable Memories", type="secondary"):
                with st.spinner("Scanning memories..."):
                    try:
                        from mirix.server.server import db_context
                        
                        org_id = st.session_state.org_id
                        user_id = st.session_state.user_id or None

                        with db_context() as session:
                            stats = memory_decay_task.get_decay_statistics(
                                session=session,
                                organization_id=org_id,
                                user_id=user_id,
                            )

                        st.session_state.cleanup_stats = stats
                        st.success("✓ Scan complete!")

                    except Exception as e:
                        st.error(f"Error scanning: {e}")
                        import traceback
                        st.code(traceback.format_exc())

        with col2:
            st.subheader("Actions")

            dry_run = st.checkbox("Dry Run (preview only)", value=True)

            if st.button("🧹 Run Cleanup", type="primary", disabled=not st.session_state.get("cleanup_stats")):
                with st.spinner("Running cleanup..."):
                    try:
                        from mirix.server.server import db_context
                        
                        org_id = st.session_state.org_id
                        user_id = st.session_state.user_id or None

                        with db_context() as session:
                            results = memory_decay_task.run_decay_cycle(
                                session=session,
                                organization_id=org_id,
                                user_id=user_id,
                                dry_run=dry_run,
                            )

                        if dry_run:
                            st.info(f"🔍 Dry run complete: Would delete {sum(results.values())} memories")
                        else:
                            st.success(f"✓ Cleanup complete: Deleted {sum(results.values())} memories")

                        st.session_state.cleanup_results = results

                    except Exception as e:
                        st.error(f"Error during cleanup: {e}")
                        import traceback
                        st.code(traceback.format_exc())

        # Display statistics
        if "cleanup_stats" in st.session_state:
            st.markdown("---")
            st.subheader("📊 Forgettable Memory Statistics")

            stats = st.session_state.cleanup_stats

            # Create summary table
            summary_data = []
            for memory_type, type_stats in stats.items():
                if isinstance(type_stats, dict) and "total_forgettable" in type_stats:
                    summary_data.append({
                        "Memory Type": memory_type,
                        "Forgettable Count": type_stats["total_forgettable"],
                    })

            if summary_data:
                df = pd.DataFrame(summary_data)
                st.dataframe(df, use_container_width=True)

                # Pie chart of forgettable memories
                fig = px.pie(
                    df,
                    values="Forgettable Count",
                    names="Memory Type",
                    title="Forgettable Memories by Type"
                )
                st.plotly_chart(fig, use_container_width=True)

        # Display results
        if "cleanup_results" in st.session_state:
            st.markdown("---")
            st.subheader("✅ Cleanup Results")

            results = st.session_state.cleanup_results
            result_data = [
                {"Memory Type": k, "Deleted/Would Delete": v}
                for k, v in results.items()
            ]
            df_results = pd.DataFrame(result_data)
            st.dataframe(df_results, use_container_width=True)

    def render_analytics(self):
        """Render analytics and visualizations"""
        st.header("📈 Memory Analytics")

        if "session" not in st.session_state or not st.session_state.session:
            st.info("Connect database to view analytics")
            return

        try:
            from mirix.server.server import db_context
            
            with db_context() as session:
                org_id = st.session_state.org_id
                user_id = st.session_state.user_id or None

                # Access frequency distribution
                st.subheader("Access Frequency Distribution")
                self.render_access_frequency_chart(session, org_id, user_id)

                st.markdown("---")

                # Importance vs Age scatter
                st.subheader("Importance vs Age Correlation")
                self.render_importance_age_scatter(session, org_id, user_id)

                st.markdown("---")

                # Rehearsal statistics
                st.subheader("Rehearsal Statistics")
                self.render_rehearsal_stats(session, org_id, user_id)

        except Exception as e:
            st.error(f"Error rendering analytics: {e}")
            import traceback
            st.code(traceback.format_exc())

    def render_access_frequency_chart(self, session, org_id, user_id):
        """Render access frequency histogram"""
        try:
            data = []
            for memory_type in MEMORY_TYPES:
                query = session.query(
                    memory_type.access_count
                ).filter(memory_type.organization_id == org_id)

                if user_id:
                    query = query.filter(memory_type.user_id == user_id)

                counts = [row[0] for row in query.all()]
                for count in counts:
                    data.append({
                        "Type": memory_type.__name__.replace("Memory", "").replace("Item", ""),
                        "Access Count": count
                    })

            if data:
                df = pd.DataFrame(data)
                fig = px.histogram(
                    df,
                    x="Access Count",
                    color="Type",
                    nbins=50,
                    title="Memory Access Frequency Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No access data available")

        except Exception as e:
            st.error(f"Error rendering access frequency: {e}")

    def render_importance_age_scatter(self, session, org_id, user_id):
        """Render importance vs age scatter plot"""
        try:
            from mirix.services.temporal_reasoning_service import temporal_service

            current_time = datetime.now(timezone.utc)
            data = []

            for memory_type in MEMORY_TYPES:
                query = session.query(memory_type).filter(
                    memory_type.organization_id == org_id
                )

                if user_id:
                    query = query.filter(memory_type.user_id == user_id)

                memories = query.limit(500).all()  # Limit for performance

                for memory in memories:
                    age = temporal_service.calculate_age_in_days(memory, current_time)
                    data.append({
                        "Type": memory_type.__name__.replace("Memory", "").replace("Item", ""),
                        "Age (days)": age,
                        "Importance Score": memory.importance_score,
                        "Access Count": memory.access_count
                    })

            if data:
                df = pd.DataFrame(data)
                fig = px.scatter(
                    df,
                    x="Age (days)",
                    y="Importance Score",
                    color="Type",
                    size="Access Count",
                    title="Memory Importance vs Age",
                    hover_data=["Access Count"]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No memory data available")

        except Exception as e:
            st.error(f"Error rendering scatter plot: {e}")

    def render_rehearsal_stats(self, session, org_id, user_id):
        """Render rehearsal statistics"""
        try:
            col1, col2, col3 = st.columns(3)

            total_rehearsed = 0
            max_rehearsal = 0
            avg_rehearsal = 0

            for memory_type in MEMORY_TYPES:
                query = session.query(
                    memory_type.rehearsal_count
                ).filter(memory_type.organization_id == org_id)

                if user_id:
                    query = query.filter(memory_type.user_id == user_id)

                counts = [row[0] for row in query.all()]
                if counts:
                    total_rehearsed += sum(1 for c in counts if c > 0)
                    max_rehearsal = max(max_rehearsal, max(counts))
                    avg_rehearsal = sum(counts) / len(counts)

            with col1:
                st.metric("Memories Rehearsed", total_rehearsed)

            with col2:
                st.metric("Max Rehearsal Count", max_rehearsal)

            with col3:
                st.metric("Avg Rehearsal Count", f"{avg_rehearsal:.2f}")

        except Exception as e:
            st.error(f"Error rendering rehearsal stats: {e}")

    def calculate_avg_importance(self, session, org_id, user_id):
        """Calculate average importance across all memories"""
        try:
            total_importance = 0
            total_count = 0

            for memory_type in MEMORY_TYPES:
                query = session.query(
                    memory_type.importance_score
                ).filter(memory_type.organization_id == org_id)

                if user_id:
                    query = query.filter(memory_type.user_id == user_id)

                scores = [row[0] for row in query.all()]
                if scores:
                    total_importance += sum(scores)
                    total_count += len(scores)

            return total_importance / total_count if total_count > 0 else 0.0

        except Exception as e:
            logger.error(f"Error calculating avg importance: {e}")
            return 0.0

    def calculate_avg_age(self, session, org_id, user_id):
        """Calculate average memory age in days"""
        try:
            from mirix.services.temporal_reasoning_service import temporal_service

            current_time = datetime.now(timezone.utc)
            total_age = 0
            total_count = 0

            for memory_type in MEMORY_TYPES:
                query = session.query(memory_type).filter(
                    memory_type.organization_id == org_id
                )

                if user_id:
                    query = query.filter(memory_type.user_id == user_id)

                memories = query.limit(1000).all()  # Limit for performance

                for memory in memories:
                    age = temporal_service.calculate_age_in_days(memory, current_time)
                    total_age += age
                    total_count += 1

            return total_age / total_count if total_count > 0 else 0.0

        except Exception as e:
            logger.error(f"Error calculating avg age: {e}")
            return 0.0

    def render_database_view(self):
        """Render database view with all memory records"""
        st.header("🗄️ Database View - Raw Memory Records")
        
        if "session" not in st.session_state or not st.session_state.session:
            st.warning("⚠️ Database not connected. Click 'Connect to Database' in sidebar.")
            return
        
        if not st.session_state.get("org_id"):
            st.warning("⚠️ Please enter an Organization ID in the sidebar.")
            return
        
        try:
            from mirix.server.server import db_context
            
            # Memory type selector
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                memory_type_names = {
                    "Chat Messages": "ChatMessage",
                    "Episodic Events": "EpisodicEvent",
                    "Semantic Memories": "SemanticMemoryItem",
                    "Procedural Memories": "ProceduralMemoryItem",
                    "Resource Memories": "ResourceMemoryItem",
                    "Knowledge Vault": "KnowledgeVaultItem"
                }
                
                selected_type_name = st.selectbox(
                    "Select Memory Type",
                    options=list(memory_type_names.keys()),
                    help="Choose which memory type to view"
                )
                
                selected_type = memory_type_names[selected_type_name]
            
            with col2:
                limit = st.number_input(
                    "Records per page",
                    min_value=10,
                    max_value=500,
                    value=50,
                    step=10,
                    help="Number of records to display"
                )
            
            with col3:
                if st.button("🔄 Refresh Data"):
                    st.rerun()
            
            # Get the ORM class
            memory_class = None
            for mem_type in MEMORY_TYPES:
                if mem_type.__name__ == selected_type:
                    memory_class = mem_type
                    break
            
            if not memory_class:
                st.error(f"Memory type {selected_type} not found")
                return
            
            # Query database
            with db_context() as session:
                org_id = st.session_state.org_id
                user_id = st.session_state.user_id or None
                
                # Build query
                query = session.query(memory_class).filter(
                    memory_class.organization_id == org_id
                )
                
                if user_id:
                    query = query.filter(memory_class.user_id == user_id)
                
                # Get total count
                total_count = query.count()
                
                # Sorting options
                st.markdown("---")
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    sort_options = {
                        "Created Date (Newest First)": "created_desc",
                        "Created Date (Oldest First)": "created_asc",
                        "Importance (High to Low)": "importance_desc",
                        "Importance (Low to High)": "importance_asc",
                        "Access Count (High to Low)": "access_desc",
                        "Access Count (Low to High)": "access_asc",
                        "Temporal Score (High to Low)": "temporal_desc",
                        "Temporal Score (Low to High)": "temporal_asc"
                    }
                    
                    sort_by = st.selectbox("Sort By", options=list(sort_options.keys()))
                    sort_key = sort_options[sort_by]
                
                with col2:
                    # Pagination
                    total_pages = (total_count + limit - 1) // limit
                    page = st.number_input(
                        "Page",
                        min_value=1,
                        max_value=max(1, total_pages),
                        value=1,
                        help=f"Total: {total_pages} pages"
                    )
                
                with col3:
                    st.metric("Total Records", total_count)
                
                # Apply sorting
                if "created" in sort_key:
                    # Try different timestamp fields based on memory type
                    if hasattr(memory_class, 'occurred_at'):
                        sort_field = memory_class.occurred_at
                    elif hasattr(memory_class, 'created_at'):
                        sort_field = memory_class.created_at
                    else:
                        sort_field = memory_class.id
                    
                    if "desc" in sort_key:
                        query = query.order_by(sort_field.desc())
                    else:
                        query = query.order_by(sort_field.asc())
                
                elif "importance" in sort_key:
                    if "desc" in sort_key:
                        query = query.order_by(memory_class.importance_score.desc())
                    else:
                        query = query.order_by(memory_class.importance_score.asc())
                
                elif "access" in sort_key:
                    if "desc" in sort_key:
                        query = query.order_by(memory_class.access_count.desc())
                    else:
                        query = query.order_by(memory_class.access_count.asc())
                
                # For temporal score, we need to calculate it
                # For simplicity, just use importance as proxy
                elif "temporal" in sort_key:
                    if "desc" in sort_key:
                        query = query.order_by(memory_class.importance_score.desc())
                    else:
                        query = query.order_by(memory_class.importance_score.asc())
                
                # Apply pagination
                offset = (page - 1) * limit
                memories = query.offset(offset).limit(limit).all()
                
                if not memories:
                    st.info(f"No {selected_type_name} found for this organization/user.")
                    return
                
                # Display summary
                st.markdown("---")
                st.subheader(f"📋 {selected_type_name} Records (Page {page} of {total_pages})")
                st.caption(f"Showing {len(memories)} of {total_count} records")
                
                # Prepare data for display
                current_time = datetime.now(timezone.utc)
                rows = []
                
                for memory in memories:
                    # Calculate temporal metrics
                    age_days = temporal_service.calculate_age_in_days(memory, current_time)
                    temporal_score = temporal_service.calculate_temporal_score(memory, current_time)
                    should_delete, delete_reason = temporal_service.should_delete(memory, current_time)
                    
                    # Get timestamp field
                    if hasattr(memory, 'occurred_at'):
                        timestamp = memory.occurred_at
                    elif hasattr(memory, 'created_at'):
                        timestamp = memory.created_at
                    else:
                        timestamp = None
                    
                    # Get content field (varies by type)
                    content = ""
                    if hasattr(memory, 'summary'):
                        content = str(memory.summary)[:100]
                    elif hasattr(memory, 'content'):
                        content = str(memory.content)[:100]
                    elif hasattr(memory, 'description'):
                        content = str(memory.description)[:100]
                    elif hasattr(memory, 'skill_name'):
                        content = str(memory.skill_name)[:100]
                    elif hasattr(memory, 'resource_name'):
                        content = str(memory.resource_name)[:100]
                    elif hasattr(memory, 'title'):
                        content = str(memory.title)[:100]
                    
                    row = {
                        "ID": str(memory.id)[:8],
                        "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M") if timestamp else "N/A",
                        "Content Preview": content,
                        "Age (days)": f"{age_days:.1f}",
                        "Importance": f"{memory.importance_score:.3f}",
                        "Access Count": memory.access_count,
                        "Rehearsal Count": memory.rehearsal_count,
                        "Last Accessed": memory.last_accessed_at.strftime("%Y-%m-%d") if memory.last_accessed_at else "Never",
                        "Temporal Score": f"{temporal_score:.3f}",
                        "Status": "🔴 Forgettable" if should_delete else "✅ Keep"
                    }
                    rows.append(row)
                
                # Display as dataframe
                df = pd.DataFrame(rows)
                
                # Style the dataframe
                def highlight_status(row):
                    if row["Status"] == "🔴 Forgettable":
                        return ['background-color: #ffcccc'] * len(row)
                    elif float(row["Importance"]) >= 0.7:
                        return ['background-color: #ccffcc'] * len(row)
                    else:
                        return [''] * len(row)
                
                styled_df = df.style.apply(highlight_status, axis=1)
                st.dataframe(styled_df, use_container_width=True, height=400)
                
                # Legend
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption("✅ Keep - Will be retained")
                with col2:
                    st.caption("🟢 High Importance (≥0.7)")
                with col3:
                    st.caption("🔴 Forgettable - Eligible for deletion")
                
                # Record detail viewer
                st.markdown("---")
                st.subheader("🔍 Record Detail Viewer")
                
                # Select record to view
                record_ids = [str(m.id) for m in memories]
                selected_id = st.selectbox(
                    "Select a record to view details",
                    options=record_ids,
                    format_func=lambda x: f"{x[:8]}... - {rows[record_ids.index(x)]['Content Preview']}"
                )
                
                if selected_id:
                    # Find the selected memory
                    selected_memory = next((m for m in memories if str(m.id) == selected_id), None)
                    
                    if selected_memory:
                        # Display in columns
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.markdown("### 📝 Basic Information")
                            st.write(f"**ID:** `{selected_memory.id}`")
                            st.write(f"**Organization ID:** `{selected_memory.organization_id}`")
                            st.write(f"**User ID:** `{selected_memory.user_id}`")
                            
                            # Type-specific fields
                            if hasattr(selected_memory, 'event_type'):
                                st.write(f"**Event Type:** {selected_memory.event_type}")
                            if hasattr(selected_memory, 'concept_type'):
                                st.write(f"**Concept Type:** {selected_memory.concept_type}")
                            if hasattr(selected_memory, 'resource_type'):
                                st.write(f"**Resource Type:** {selected_memory.resource_type}")
                            if hasattr(selected_memory, 'category'):
                                st.write(f"**Category:** {selected_memory.category}")
                            if hasattr(selected_memory, 'role'):
                                st.write(f"**Role:** {selected_memory.role}")
                            if hasattr(selected_memory, 'session_id'):
                                st.write(f"**Session ID:** `{selected_memory.session_id}`")
                        
                        with col2:
                            st.markdown("### ⏱️ Temporal Metrics")
                            age_days = temporal_service.calculate_age_in_days(selected_memory, current_time)
                            decay_factor = temporal_service.calculate_decay_factor(selected_memory, current_time)
                            recency_bonus = temporal_service.calculate_recency_bonus(selected_memory, current_time)
                            frequency_score = temporal_service.calculate_frequency_score(selected_memory)
                            temporal_score = temporal_service.calculate_temporal_score(selected_memory, current_time)
                            should_delete, delete_reason = temporal_service.should_delete(selected_memory, current_time)
                            
                            st.write(f"**Age:** {age_days:.2f} days")
                            st.write(f"**Importance:** {selected_memory.importance_score:.4f}")
                            st.write(f"**Access Count:** {selected_memory.access_count}")
                            st.write(f"**Rehearsal Count:** {selected_memory.rehearsal_count}")
                            st.write(f"**Decay Factor:** {decay_factor:.4f}")
                            st.write(f"**Recency Bonus:** {recency_bonus:.4f}")
                            st.write(f"**Frequency Score:** {frequency_score:.4f}")
                            st.write(f"**Temporal Score:** {temporal_score:.4f}")
                            st.write(f"**Status:** {'🔴 Forgettable' if should_delete else '✅ Keep'}")
                            if delete_reason:
                                st.write(f"**Reason:** {delete_reason}")
                        
                        # Content
                        st.markdown("### 📄 Content")
                        if hasattr(selected_memory, 'summary'):
                            st.write(f"**Summary:** {selected_memory.summary}")
                            if hasattr(selected_memory, 'details'):
                                st.text_area("Details", selected_memory.details, height=150, disabled=True)
                        elif hasattr(selected_memory, 'content'):
                            st.text_area("Full Content", selected_memory.content, height=150, disabled=True)
                        elif hasattr(selected_memory, 'description'):
                            st.text_area("Description", selected_memory.description, height=150, disabled=True)
                        elif hasattr(selected_memory, 'skill_name'):
                            st.write(f"**Skill:** {selected_memory.skill_name}")
                            if hasattr(selected_memory, 'description'):
                                st.text_area("Description", selected_memory.description, height=100, disabled=True)
                        elif hasattr(selected_memory, 'resource_name'):
                            st.write(f"**Resource:** {selected_memory.resource_name}")
                            if hasattr(selected_memory, 'description'):
                                st.text_area("Description", selected_memory.description, height=100, disabled=True)
                        elif hasattr(selected_memory, 'title'):
                            st.write(f"**Title:** {selected_memory.title}")
                            if hasattr(selected_memory, 'content'):
                                st.text_area("Content", selected_memory.content, height=100, disabled=True)
                        
                        # Metadata
                        if hasattr(selected_memory, 'metadata_') and selected_memory.metadata_:
                            st.markdown("### 🏷️ Metadata")
                            st.json(selected_memory.metadata_)
                        
                        if hasattr(selected_memory, 'last_modify') and selected_memory.last_modify:
                            st.markdown("### 🔄 Last Modification")
                            st.json(selected_memory.last_modify)
                        
                        # Raw JSON view
                        with st.expander("🔧 View Raw JSON"):
                            # Convert SQLAlchemy object to dict
                            raw_dict = {}
                            for column in selected_memory.__table__.columns:
                                value = getattr(selected_memory, column.name)
                                # Handle datetime serialization
                                if isinstance(value, datetime):
                                    raw_dict[column.name] = value.isoformat()
                                else:
                                    raw_dict[column.name] = value
                            st.json(raw_dict)
                
                # Export options
                st.markdown("---")
                st.subheader("📥 Export Data")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📊 Export Current Page as CSV"):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv,
                            file_name=f"{selected_type}_{org_id}_page{page}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("📋 Export All Records as CSV"):
                        # Query all records
                        all_memories = query.all()
                        all_rows = []
                        
                        for memory in all_memories:
                            age_days = temporal_service.calculate_age_in_days(memory, current_time)
                            temporal_score = temporal_service.calculate_temporal_score(memory, current_time)
                            
                            if hasattr(memory, 'occurred_at'):
                                timestamp = memory.occurred_at
                            elif hasattr(memory, 'created_at'):
                                timestamp = memory.created_at
                            else:
                                timestamp = None
                            
                            content = ""
                            if hasattr(memory, 'summary'):
                                content = str(memory.summary)
                                if hasattr(memory, 'details'):
                                    content += " - " + str(memory.details)
                            elif hasattr(memory, 'content'):
                                content = str(memory.content)
                            elif hasattr(memory, 'description'):
                                content = str(memory.description)
                            
                            all_rows.append({
                                "ID": str(memory.id),
                                "Timestamp": timestamp.isoformat() if timestamp else "",
                                "Content": content,
                                "Age_Days": age_days,
                                "Importance": memory.importance_score,
                                "Access_Count": memory.access_count,
                                "Rehearsal_Count": memory.rehearsal_count,
                                "Temporal_Score": temporal_score
                            })
                        
                        all_df = pd.DataFrame(all_rows)
                        csv_all = all_df.to_csv(index=False)
                        st.download_button(
                            label=f"⬇️ Download All {total_count} Records",
                            data=csv_all,
                            file_name=f"{selected_type}_{org_id}_all.csv",
                            mime="text/csv"
                        )
                
                with col3:
                    if st.button("🗑️ Delete Selected Record"):
                        st.warning("⚠️ Delete functionality coming soon...")
                        # TODO: Implement safe deletion with confirmation
        
        except Exception as e:
            st.error(f"Error loading database view: {e}")
            import traceback
            st.code(traceback.format_exc())


def run_ui():
    """Run the Streamlit UI"""
    ui = TemporalReasoningUI()
    ui.render()


if __name__ == "__main__":
    run_ui()

