# lambda/index.py
"""
Lambda関数のハンドラー
FastAPIで実装した推論APIに接続して推論を行う

主な機能:
- API Gatewayからのリクエストを受け取り、FastAPIエンドポイントに転送
- 会話履歴の管理と更新
- エラーハンドリングと適切なレスポンスの返却

制限事項:
- リクエストボディには'message'と'conversationHistory'が必要
- FastAPIエンドポイントのURLは環境変数で設定可能
"""

import json
import urllib.request
import urllib.parse
import re
import os


def extract_region_from_arn(arn):
    """
    Lambda コンテキストからリージョンを抽出する関数
    
    Args:
        arn (str): Lambda関数のARN
    
    Returns:
        str: リージョン名（デフォルト: us-east-1）
    """
    # ARN 形式: arn:aws:lambda:region:account-id:function:function-name
    match = re.search('arn:aws:lambda:([^:]+):', arn)
    if match:
        return match.group(1)
    return "us-east-1"  # デフォルト値


# FastAPIエンドポイントのURL（環境変数から取得、デフォルト値は演習用のURL）
FASTAPI_URL = os.environ.get('FASTAPI_URL', 'https://f515-34-145-165-103.ngrok-free.app/generate')


def lambda_handler(event, context):
    """
    Lambda関数のハンドラー
    FastAPIで実装した推論APIに接続して推論を行う
    
    Args:
        event (dict): API Gatewayからのイベントデータ
        context (object): Lambdaコンテキスト
    
    Returns:
        dict: API Gatewayのレスポンス形式に準拠した応答
    """
    try:
        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body.get('message', '')
        conversation_history = body.get('conversationHistory', [])
        
        if not message:
            return {
                'statusCode': 400,
                'headers': {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": (
                        "Content-Type,X-Amz-Date,Authorization,"
                        "X-Api-Key,X-Amz-Security-Token"
                    ),
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'メッセージが指定されていません'
                })
            }
        
        # リクエストデータの準備
        request_data = {
            "prompt": message,
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        # リクエストの送信
        req = urllib.request.Request(
            FASTAPI_URL,
            data=json.dumps(request_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
                # アシスタントの応答を会話履歴に追加
                messages = conversation_history.copy()
                messages.append({
                    "role": "user",
                    "content": message
                })
                messages.append({
                    "role": "assistant",
                    "content": response_data['generated_text']
                })
                
                return {
                    'statusCode': 200,
                    'headers': {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": (
                            "Content-Type,X-Amz-Date,Authorization,"
                            "X-Api-Key,X-Amz-Security-Token"
                        ),
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    'body': json.dumps({
                        'success': True,
                        'response': response_data['generated_text'],
                        'conversationHistory': messages
                    })
                }
                
        except urllib.error.HTTPError as e:
            error_message = f"FastAPIエンドポイントへのリクエストに失敗しました: {str(e)}"
            print(error_message)
            return {
                'statusCode': e.code,
                'headers': {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": (
                        "Content-Type,X-Amz-Date,Authorization,"
                        "X-Api-Key,X-Amz-Security-Token"
                    ),
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                'body': json.dumps({
                    'success': False,
                    'error': error_message
                })
            }
            
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": (
                    "Content-Type,X-Amz-Date,Authorization,"
                    "X-Api-Key,X-Amz-Security-Token"
                ),
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            'body': json.dumps({
                'success': False,
                'error': 'リクエストボディのJSON形式が不正です'
            })
        }
            
    except Exception as error:
        print("Error:", str(error))
        
        return {
            'statusCode': 500,
            'headers': {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": (
                    "Content-Type,X-Amz-Date,Authorization,"
                    "X-Api-Key,X-Amz-Security-Token"
                ),
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            'body': json.dumps({
                'success': False,
                'error': str(error)
            })
        }
