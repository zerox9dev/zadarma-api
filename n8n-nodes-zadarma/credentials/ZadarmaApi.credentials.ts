import {
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class ZadarmaApi implements ICredentialType {
	name = 'zadarmaApi';
	displayName = 'Zadarma API';
	documentationUrl = 'https://zadarma.com/en/support/api/';
	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
			description: 'Your Zadarma API Key from https://my.zadarma.com/api/',
		},
		{
			displayName: 'API Secret',
			name: 'apiSecret',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
			description: 'Your Zadarma API Secret from https://my.zadarma.com/api/',
		},
		{
			displayName: 'Sandbox Mode',
			name: 'sandbox',
			type: 'boolean',
			default: false,
			description: 'Whether to use the sandbox environment for testing',
		},
	];
}