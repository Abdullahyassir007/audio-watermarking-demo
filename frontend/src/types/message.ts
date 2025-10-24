// Message payload types
export type MessageFormat = 'numeric' | 'text' | 'binary';

export interface MessagePayload {
  format: MessageFormat;
  values: number[]; // Always 5 integers 0-255
  originalInput: string | number[];
}
