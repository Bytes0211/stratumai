"""Tests for AWS Bedrock provider."""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from llm_abstraction.providers.bedrock import BedrockProvider
from llm_abstraction.models import ChatRequest, Message, Usage
from llm_abstraction.exceptions import AuthenticationError, InvalidModelError, ProviderAPIError


class TestBedrockProviderInitialization:
    """Tests for Bedrock provider initialization."""
    
    def test_initialization_with_credentials(self):
        """Test provider initialization with explicit AWS credentials."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key-id",
                aws_secret_access_key="test-secret-key"
            )
            assert provider.aws_access_key_id == "test-key-id"
            assert provider.aws_secret_access_key == "test-secret-key"
            assert provider.region_name == "us-east-1"  # default
            assert provider.provider_name == "bedrock"
    
    def test_initialization_with_env_vars(self):
        """Test provider initialization with environment variables."""
        with patch.dict("os.environ", {
            "AWS_ACCESS_KEY_ID": "env-key-id",
            "AWS_SECRET_ACCESS_KEY": "env-secret-key",
            "AWS_DEFAULT_REGION": "us-west-2"
        }):
            with patch("llm_abstraction.providers.bedrock.boto3.Session"):
                provider = BedrockProvider()
                assert provider.aws_access_key_id == "env-key-id"
                assert provider.aws_secret_access_key == "env-secret-key"
                assert provider.region_name == "us-west-2"
    
    def test_initialization_with_custom_region(self):
        """Test provider initialization with custom region."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret",
                region_name="eu-west-1"
            )
            assert provider.region_name == "eu-west-1"
    
    def test_initialization_with_session_token(self):
        """Test provider initialization with session token."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret",
                aws_session_token="test-token"
            )
            assert provider.aws_session_token == "test-token"
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_initialization_creates_bedrock_client(self, mock_session_class):
        """Test that initialization creates bedrock-runtime client."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        
        mock_session.client.assert_called_once_with("bedrock-runtime")
        assert provider._client == mock_client


class TestBedrockProviderModels:
    """Tests for Bedrock provider model support."""
    
    def test_supported_models(self):
        """Test that provider returns list of supported Bedrock models."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret"
            )
            models = provider.get_supported_models()
            
            assert isinstance(models, list)
            assert len(models) > 0
            
            # Check for key models from each family
            assert "anthropic.claude-3-5-sonnet-20241022-v2:0" in models
            assert "meta.llama3-3-70b-instruct-v1:0" in models
            assert "mistral.mistral-large-2407-v1:0" in models
            assert "amazon.titan-text-premier-v1:0" in models
            assert "cohere.command-r-plus-v1:0" in models
    
    def test_validate_model(self):
        """Test model validation."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret"
            )
            
            # Valid models
            assert provider.validate_model("anthropic.claude-3-5-sonnet-20241022-v2:0") is True
            assert provider.validate_model("meta.llama3-3-70b-instruct-v1:0") is True
            
            # Invalid model
            assert provider.validate_model("invalid-model") is False


class TestBedrockProviderChatCompletion:
    """Tests for Bedrock chat completion."""
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_chat_completion_anthropic_claude(self, mock_session_class):
        """Test chat completion with Anthropic Claude model."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        mock_response = {
            "body": MagicMock()
        }
        mock_response["body"].read.return_value = json.dumps({
            "id": "msg_123",
            "content": [{"type": "text", "text": "Hello from Bedrock!"}],
            "stop_reason": "end_turn",
            "usage": {
                "input_tokens": 10,
                "output_tokens": 5
            }
        }).encode()
        
        mock_client.invoke_model.return_value = mock_response
        
        # Create provider and make request
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        request = ChatRequest(
            model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[Message(role="user", content="Hello")]
        )
        
        response = provider.chat_completion(request)
        
        assert response.content == "Hello from Bedrock!"
        assert response.provider == "bedrock"
        assert response.model == "anthropic.claude-3-5-sonnet-20241022-v2:0"
        assert response.usage.prompt_tokens == 10
        assert response.usage.completion_tokens == 5
        assert response.usage.total_tokens == 15
        assert response.usage.cost_usd > 0  # Cost should be calculated
        
        # Verify API call
        mock_client.invoke_model.assert_called_once()
        call_args = mock_client.invoke_model.call_args
        assert call_args.kwargs["modelId"] == "anthropic.claude-3-5-sonnet-20241022-v2:0"
        assert call_args.kwargs["contentType"] == "application/json"
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_chat_completion_llama(self, mock_session_class):
        """Test chat completion with Meta Llama model."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        mock_response = {
            "body": MagicMock()
        }
        mock_response["body"].read.return_value = json.dumps({
            "generation": "Llama response!",
            "prompt_token_count": 10,
            "generation_token_count": 8,
            "stop_reason": "stop"
        }).encode()
        
        mock_client.invoke_model.return_value = mock_response
        
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        request = ChatRequest(
            model="meta.llama3-3-70b-instruct-v1:0",
            messages=[Message(role="user", content="Hello")]
        )
        
        response = provider.chat_completion(request)
        
        assert response.content == "Llama response!"
        assert response.usage.prompt_tokens == 10
        assert response.usage.completion_tokens == 8
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_chat_completion_titan(self, mock_session_class):
        """Test chat completion with Amazon Titan model."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        mock_response = {
            "body": MagicMock()
        }
        mock_response["body"].read.return_value = json.dumps({
            "results": [{
                "outputText": "Titan response!",
                "inputTextTokenCount": 12,
                "outputTextTokenCount": 6,
                "completionReason": "FINISH"
            }]
        }).encode()
        
        mock_client.invoke_model.return_value = mock_response
        
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        request = ChatRequest(
            model="amazon.titan-text-premier-v1:0",
            messages=[Message(role="user", content="Hello")]
        )
        
        response = provider.chat_completion(request)
        
        assert response.content == "Titan response!"
        assert response.usage.prompt_tokens == 12
        assert response.usage.completion_tokens == 6
    
    def test_chat_completion_invalid_model(self):
        """Test chat completion with invalid model raises error."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret"
            )
            request = ChatRequest(
                model="invalid-model",
                messages=[Message(role="user", content="Hello")]
            )
            
            with pytest.raises(InvalidModelError):
                provider.chat_completion(request)
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_chat_completion_with_system_message(self, mock_session_class):
        """Test chat completion with system message."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        mock_response = {
            "body": MagicMock()
        }
        mock_response["body"].read.return_value = json.dumps({
            "content": [{"type": "text", "text": "Response"}],
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 15, "output_tokens": 5}
        }).encode()
        
        mock_client.invoke_model.return_value = mock_response
        
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        request = ChatRequest(
            model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[
                Message(role="system", content="You are helpful"),
                Message(role="user", content="Hello")
            ]
        )
        
        response = provider.chat_completion(request)
        
        # Verify system message was included in request
        call_args = mock_client.invoke_model.call_args
        body = json.loads(call_args.kwargs["body"])
        assert "system" in body
        assert body["system"] == "You are helpful"


class TestBedrockProviderStreaming:
    """Tests for Bedrock streaming."""
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_chat_completion_stream_anthropic(self, mock_session_class):
        """Test streaming chat completion with Anthropic Claude."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        # Mock streaming response
        mock_event1 = {
            "chunk": {
                "bytes": json.dumps({
                    "type": "content_block_delta",
                    "delta": {"text": "Hello"}
                }).encode()
            }
        }
        mock_event2 = {
            "chunk": {
                "bytes": json.dumps({
                    "type": "content_block_delta",
                    "delta": {"text": " world"}
                }).encode()
            }
        }
        
        mock_stream = [mock_event1, mock_event2]
        mock_response = {"body": mock_stream}
        mock_client.invoke_model_with_response_stream.return_value = mock_response
        
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        request = ChatRequest(
            model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[Message(role="user", content="Hello")],
            stream=True
        )
        
        chunks = list(provider.chat_completion_stream(request))
        
        assert len(chunks) == 2
        assert chunks[0].content == "Hello"
        assert chunks[1].content == " world"
        assert all(chunk.provider == "bedrock" for chunk in chunks)
    
    def test_chat_completion_stream_invalid_model(self):
        """Test streaming with invalid model raises error."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret"
            )
            request = ChatRequest(
                model="invalid-model",
                messages=[Message(role="user", content="Hello")],
                stream=True
            )
            
            with pytest.raises(InvalidModelError):
                list(provider.chat_completion_stream(request))


class TestBedrockProviderCostCalculation:
    """Tests for cost calculation."""
    
    def test_calculate_cost_claude(self):
        """Test cost calculation for Claude model."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret"
            )
            
            usage = Usage(
                prompt_tokens=1000,
                completion_tokens=500,
                total_tokens=1500
            )
            
            cost = provider._calculate_cost(usage, "anthropic.claude-3-5-sonnet-20241022-v2:0")
            
            # Claude 3.5 Sonnet pricing: $3/MTok input, $15/MTok output
            expected_cost = (1000 / 1_000_000) * 3.0 + (500 / 1_000_000) * 15.0
            assert cost == pytest.approx(expected_cost)
    
    def test_calculate_cost_llama(self):
        """Test cost calculation for Llama model."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret"
            )
            
            usage = Usage(
                prompt_tokens=2000,
                completion_tokens=1000,
                total_tokens=3000
            )
            
            cost = provider._calculate_cost(usage, "meta.llama3-3-70b-instruct-v1:0")
            
            # Llama 3.3 70B pricing: $0.99/MTok for both input and output
            expected_cost = (2000 / 1_000_000) * 0.99 + (1000 / 1_000_000) * 0.99
            assert cost == pytest.approx(expected_cost)


class TestBedrockProviderRequestBuilding:
    """Tests for request body building."""
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_build_anthropic_request(self, mock_session_class):
        """Test building request body for Anthropic Claude."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_session.client.return_value = Mock()
        
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        request = ChatRequest(
            model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[Message(role="user", content="Hello")],
            temperature=0.8,
            max_tokens=1000
        )
        
        body = provider._build_request_body(request)
        
        assert body["anthropic_version"] == "bedrock-2023-05-31"
        assert body["messages"] == [{"role": "user", "content": "Hello"}]
        assert body["max_tokens"] == 1000
        assert body["temperature"] == 0.8
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_build_titan_request(self, mock_session_class):
        """Test building request body for Amazon Titan."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_session.client.return_value = Mock()
        
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        request = ChatRequest(
            model="amazon.titan-text-premier-v1:0",
            messages=[Message(role="user", content="Hello")],
            temperature=0.7,
            max_tokens=500
        )
        
        body = provider._build_request_body(request)
        
        assert "inputText" in body
        assert body["textGenerationConfig"]["maxTokenCount"] == 500
        assert body["textGenerationConfig"]["temperature"] == 0.7


class TestBedrockProviderErrorHandling:
    """Tests for error handling."""
    
    @patch("llm_abstraction.providers.bedrock.boto3.Session")
    def test_client_error_handling(self, mock_session_class):
        """Test handling of AWS ClientError."""
        from botocore.exceptions import ClientError
        
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        # Mock ClientError
        error_response = {
            "Error": {
                "Code": "ValidationException",
                "Message": "Invalid request"
            }
        }
        mock_client.invoke_model.side_effect = ClientError(error_response, "InvokeModel")
        
        provider = BedrockProvider(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        request = ChatRequest(
            model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[Message(role="user", content="Hello")]
        )
        
        with pytest.raises(ProviderAPIError) as exc_info:
            provider.chat_completion(request)
        
        assert "ValidationException" in str(exc_info.value)
    
    def test_temperature_validation(self):
        """Test temperature validation for Bedrock (0.0-1.0)."""
        with patch("llm_abstraction.providers.bedrock.boto3.Session"):
            provider = BedrockProvider(
                aws_access_key_id="test-key",
                aws_secret_access_key="test-secret"
            )
            request = ChatRequest(
                model="anthropic.claude-3-5-sonnet-20241022-v2:0",
                messages=[Message(role="user", content="Hello")],
                temperature=2.0  # Invalid for Bedrock
            )
            
            from llm_abstraction.exceptions import ValidationError
            with pytest.raises(ValidationError):
                provider.chat_completion(request)
