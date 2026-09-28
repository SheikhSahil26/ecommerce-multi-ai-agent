import { Check, Copy, Sparkles } from "lucide-react"
import { BrandMark } from "../shared/BrandMark"
import { CheckoutApproval } from "./CheckoutApproval"

export function ChatMessage({ message, onSend, busy }) {
  const assistant = message.role === "assistant"
  return <article className={`message-row ${assistant ? "assistant-message" : "user-message"}`}>
    {assistant && <div className="assistant-avatar"><BrandMark small/></div>}
    <div className="message-content">
      {assistant && <div className="message-label">COMMON GOODS <span>·</span> SHOPPING ASSISTANT</div>}
      <div className={`message-bubble ${assistant ? "assistant-bubble" : "user-bubble"}`}>{message.content}</div>
      {message.approvalRequired && <CheckoutApproval disabled={busy} onConfirm={() => onSend("Yes, I confirm. Please place the order.")} onCancel={() => onSend("No, cancel checkout. I do not want to place this order.")}/>}
      {assistant && message.id !== "welcome" && <div className="message-tools"><button onClick={() => navigator.clipboard?.writeText(message.content)}><Copy size={12}/> Copy</button><button onClick={() => onSend("Can you tell me more?")} disabled={busy}><Sparkles size={12}/> Ask a follow-up</button></div>}
    </div>
  </article>
}
