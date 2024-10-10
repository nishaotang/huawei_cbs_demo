import os,json
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig
# 导入CBS服务库huaweicloudsdkcbs
from huaweicloudsdkcbs.v1.region.cbs_region import CbsRegion
from huaweicloudsdkcbs.v1 import *

def cbsUtil(question):
    # 使用默认配置，如出现'HttpConfig' is not defined报错，请检查是否已正确安装sdk
    config = HttpConfig.get_default_config()
    # 根据需要配置是否跳过SSL证书校验
    config.ignore_ssl_verification = False

    # 默认连接超时时间为60秒，读取超时时间为120秒，支持统一指定超时时长timeout=timeout，或分别指定超时时长timeout=(connect timeout, read timeout)
    config.timeout = 10

    # 配置AK、SK、project_id信息。华为云通过AK识别用户的身份，通过SK对请求数据进行签名验证，用于确保请求的机密性、完整性和请求者身份的正确性。
    # 请勿将认证信息硬编码到代码中，有安全风险。
    ak = os.getenv('HUAWEICLOUD_SDK_AK')
    sk = os.getenv('HUAWEICLOUD_SDK_SK')
    project_id = os.getenv('HUAWEICLOUD_PROJECT_ID')
    qabot_id = os.getenv('HUAWEICLOUD_QABOT_ID')
    basic_credentials = BasicCredentials(ak, sk, project_id)
    # 初始化指定云服务的客户端 {Service}Client ，以初始化 Region 级服务CBS的 CbsClient 为例
    client = CbsClient.new_builder() \
        .with_http_config(config) \
        .with_credentials(basic_credentials) \
        .with_region(CbsRegion.value_of("cn-north-4")) \
        .build()
    try:
        request = ExecuteQaChatRequest()
        request.qabot_id = qabot_id
        request.body = PostRequestsReq(
            question = question
        )

        print(question)
        print("----")
        response = client.execute_qa_chat(request)
        print(response)
        #问答型机器人回复
        if response.reply_type == 0:
            return response.qabot_answers.answers[0].answer
        #任务型机器人回复
        elif response.reply_type == 1 :
            return response.taskbot_answers.answer
        #闲聊回复
        elif response.reply_type == 2:
            return response.chat_answers.answer
        else:
            return '请求失败'
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
        return e.error_msg
