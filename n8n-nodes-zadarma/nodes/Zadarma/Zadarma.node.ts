import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	NodeOperationError,
	NodeConnectionType,
} from 'n8n-workflow';

import { createHash, createHmac } from 'crypto';

export class Zadarma implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Zadarma',
		name: 'zadarma',
		icon: 'file:zadarma.svg',
		group: ['communication'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Interact with Zadarma API',
		defaults: {
			name: 'Zadarma',
		},
		inputs: [NodeConnectionType.Main],
		outputs: [NodeConnectionType.Main],
		credentials: [
			{
				name: 'zadarmaApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Call Statistics',
						value: 'statistics',
					},
					{
						name: 'Call Recording',
						value: 'recording',
					},
				],
				default: 'statistics',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['statistics'],
					},
				},
				options: [
					{
						name: 'Get Call Statistics',
						value: 'getStats',
						description: 'Get call statistics for a date range',
						action: 'Get call statistics',
					},
				],
				default: 'getStats',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['recording'],
					},
				},
				options: [
					{
						name: 'Get Download Link',
						value: 'getLink',
						description: 'Get download link for a call recording',
						action: 'Get recording download link',
					},
				],
				default: 'getLink',
			},
			// Call Statistics Parameters
			{
				displayName: 'Start Date',
				name: 'startDate',
				type: 'dateTime',
				displayOptions: {
					show: {
						resource: ['statistics'],
						operation: ['getStats'],
					},
				},
				default: '',
				description: 'Start date for statistics (YYYY-MM-DD HH:MM:SS format)',
				required: true,
			},
			{
				displayName: 'End Date',
				name: 'endDate',
				type: 'dateTime',
				displayOptions: {
					show: {
						resource: ['statistics'],
						operation: ['getStats'],
					},
				},
				default: '',
				description: 'End date for statistics (YYYY-MM-DD HH:MM:SS format)',
				required: true,
			},
			// Call Recording Parameters
			{
				displayName: 'Call ID',
				name: 'callId',
				type: 'string',
				displayOptions: {
					show: {
						resource: ['recording'],
						operation: ['getLink'],
					},
				},
				default: '',
				description: 'The ID of the call to get recording download link for',
				required: true,
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];

		const credentials = await this.getCredentials('zadarmaApi');
		const apiKey = credentials.apiKey as string;
		const apiSecret = credentials.apiSecret as string;
		const sandbox = credentials.sandbox as boolean;

		const baseUrl = sandbox ? 'https://api-sandbox.zadarma.com' : 'https://api.zadarma.com';

		for (let i = 0; i < items.length; i++) {
			try {
				const resource = this.getNodeParameter('resource', i) as string;
				const operation = this.getNodeParameter('operation', i) as string;

				let endpoint = '';
				let params: { [key: string]: string } = {};

				if (resource === 'statistics' && operation === 'getStats') {
					endpoint = '/v1/statistics/pbx/';
					
					const startDate = this.getNodeParameter('startDate', i) as string;
					const endDate = this.getNodeParameter('endDate', i) as string;
					
					// Convert ISO dates to Zadarma format
					const startFormatted = new Date(startDate).toISOString().slice(0, 19).replace('T', ' ');
					const endFormatted = new Date(endDate).toISOString().slice(0, 19).replace('T', ' ');
					
					params = {
						start: startFormatted,
						end: endFormatted,
						format: 'json',
					};
				} else if (resource === 'recording' && operation === 'getLink') {
					endpoint = '/v1/pbx/record/request/';
					const callId = this.getNodeParameter('callId', i) as string;
					
					params = {
						call_id: callId,
						format: 'json',
					};
				}

				// Generate signature using EXACT Python algorithm
				const zadarmaNode = new Zadarma();
				const signature = zadarmaNode.generateZadarmaSignature(endpoint, params, apiSecret);
				
				// Make API request
				const url = `${baseUrl}${endpoint}`;
				const queryString = zadarmaNode.buildQueryString(params);
				const fullUrl = `${url}?${queryString}`;

				const response = await this.helpers.request({
					method: 'GET',
					url: fullUrl,
					headers: {
						'Authorization': `${apiKey}:${signature}`,
					},
					json: true,
				});

				returnData.push({
					json: response,
					pairedItem: { item: i },
				});

			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({
						json: { error: error.message },
						pairedItem: { item: i },
					});
					continue;
				}
				throw new NodeOperationError(this.getNode(), error as Error, { itemIndex: i });
			}
		}

		return [returnData];
	}

	/**
	 * RFC1738 URL encoding (matches Python's urlencode)
	 * This differs from encodeURIComponent which uses RFC3986
	 */
	public rfc1738Encode(str: string): string {
		return encodeURIComponent(str).replace(/%20/g, '+');
	}

	/**
	 * Generate Zadarma API signature - EXACT copy of Python algorithm
	 * 🚨 CRITICAL: This matches the working Python code exactly!
	 */
	public generateZadarmaSignature(method: string, params: { [key: string]: string }, secret: string): string {
		// 1. Sort parameters alphabetically (ksort in PHP, sorted() in Python)
		const sortedParams = Object.keys(params).sort().map(key => [key, params[key]]);
		
		// 2. Create query string using RFC1738 encoding (urlencode in Python)
		// 🚨 CRITICAL: Use RFC1738 encoding (spaces as +) not RFC3986 (spaces as %20)
		const paramsString = sortedParams
			.map(([key, value]) => `${this.rfc1738Encode(key)}=${this.rfc1738Encode(value)}`)
			.join('&');
		
		// 3. MD5 hash of parameters string
		const md5Hash = createHash('md5').update(paramsString, 'utf8').digest('hex');
		
		// 4. Create string to sign: method + params_string + md5(params_string)
		const stringToSign = `${method}${paramsString}${md5Hash}`;
		
		// 5. HMAC-SHA1 with secret key
		const hmac = createHmac('sha1', secret);
		hmac.update(stringToSign, 'utf8');
		
		// 6. 🚨 CRITICAL: Base64 encode the HEX digest (not raw bytes!)
		// This matches Python: base64.b64encode(hmac_result.hexdigest().encode('utf-8'))
		const signature = Buffer.from(hmac.digest('hex'), 'utf8').toString('base64');
		
		return signature;
	}

	/**
	 * Build query string for URL - matches Python urlencode behavior
	 * 🚨 CRITICAL: Must use RFC1738 encoding (spaces as +) to match signature
	 */
	public buildQueryString(params: { [key: string]: string }): string {
		const sortedParams = Object.keys(params).sort().map(key => [key, params[key]]);
		return sortedParams
			.map(([key, value]) => `${this.rfc1738Encode(key)}=${this.rfc1738Encode(value)}`)
			.join('&');
	}
}