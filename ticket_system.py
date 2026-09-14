# Ticket System - Manages customer tickets for next-day follow-up

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import uuid


class TicketSystem:
    """Manages customer support tickets"""
    
    def __init__(self, storage_dir='tickets'):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        self.open_tickets_file = os.path.join(storage_dir, 'open_tickets.json')
        self.resolved_tickets_file = os.path.join(storage_dir, 'resolved_tickets.json')
        
        # Initialize files if they don't exist
        if not os.path.exists(self.open_tickets_file):
            self._save_tickets(self.open_tickets_file, [])
        if not os.path.exists(self.resolved_tickets_file):
            self._save_tickets(self.resolved_tickets_file, [])
    
    def _save_tickets(self, filepath: str, tickets: List[Dict]):
        """Save tickets to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    def _load_tickets(self, filepath: str) -> List[Dict]:
        """Load tickets from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def create_ticket(
        self,
        customer_phone: str,
        question: str,
        sentiment: Dict,
        conversation_history: List[str],
        reason: str,
        category: str = 'general',
        suggested_action: str = None
    ) -> Dict:
        """Create a new support ticket"""
        
        # Generate ticket ID
        date_str = datetime.now().strftime('%Y%m%d')
        open_tickets = self._load_tickets(self.open_tickets_file)
        ticket_number = len(open_tickets) + 1
        ticket_id = f"TKT-{date_str}-{ticket_number:03d}"
        
        # Create ticket object
        ticket = {
            'ticket_id': ticket_id,
            'timestamp': datetime.now().isoformat(),
            'customer_phone': customer_phone,
            'customer_name': None,  # Can be populated later
            'question': question,
            'conversation_history': conversation_history,
            'sentiment': sentiment,
            'priority': self._determine_priority(sentiment, reason),
            'category': category,
            'escalation_reason': reason,
            'suggested_action': suggested_action or self._suggest_action(question, sentiment),
            'status': 'open',
            'assigned_to': None,
            'resolved_at': None,
            'resolution_notes': None
        }
        
        # Save ticket
        open_tickets.append(ticket)
        self._save_tickets(self.open_tickets_file, open_tickets)
        
        return ticket
    
    def _determine_priority(self, sentiment: Dict, reason: str) -> str:
        """Determine ticket priority based on sentiment and reason"""
        
        if sentiment['sentiment'] == 'negative':
            if sentiment['score'] <= -3:
                return 'urgent'
            return 'high'
        
        if reason == 'high_priority':
            return 'high'
        
        if sentiment['priority'] == 'medium':
            return 'medium'
        
        return 'low'
    
    def _suggest_action(self, question: str, sentiment: Dict) -> str:
        """Suggest action for the support team"""
        
        question_lower = question.lower()
        
        if 'retour' in question_lower or 'terugsturen' in question_lower:
            return 'Check order status, explain return policy, provide return label'
        
        if 'klacht' in question_lower or 'complaint' in question_lower:
            return 'Apologize, investigate issue, offer compensation if appropriate'
        
        if 'technisch' in question_lower or 'technical' in question_lower:
            return 'Forward to technical support team'
        
        if 'betaling' in question_lower or 'payment' in question_lower:
            return 'Check payment status, forward to finance if needed'
        
        if sentiment['sentiment'] == 'negative':
            return 'Priority callback within 2 hours, empathetic approach'
        
        return 'Review question, provide accurate answer during work hours'
    
    def resolve_ticket(self, ticket_id: str, resolution_notes: str, assigned_to: str = None) -> bool:
        """Mark a ticket as resolved"""
        
        open_tickets = self._load_tickets(self.open_tickets_file)
        
        # Find and remove ticket from open list
        ticket_index = None
        for i, ticket in enumerate(open_tickets):
            if ticket['ticket_id'] == ticket_id:
                ticket_index = i
                break
        
        if ticket_index is None:
            return False
        
        # Update ticket
        ticket = open_tickets.pop(ticket_index)
        ticket['status'] = 'resolved'
        ticket['resolved_at'] = datetime.now().isoformat()
        ticket['resolution_notes'] = resolution_notes
        if assigned_to:
            ticket['assigned_to'] = assigned_to
        
        # Save to resolved tickets
        resolved_tickets = self._load_tickets(self.resolved_tickets_file)
        resolved_tickets.append(ticket)
        self._save_tickets(self.resolved_tickets_file, resolved_tickets)
        
        # Save updated open tickets
        self._save_tickets(self.open_tickets_file, open_tickets)
        
        return True
    
    def get_open_tickets(self, priority: str = None) -> List[Dict]:
        """Get all open tickets, optionally filtered by priority"""
        
        tickets = self._load_tickets(self.open_tickets_file)
        
        if priority:
            tickets = [t for t in tickets if t['priority'] == priority]
        
        # Sort by priority and timestamp
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
        tickets.sort(key=lambda x: (priority_order.get(x['priority'], 4), x['timestamp']))
        
        return tickets
    
    def get_ticket_stats(self) -> Dict:
        """Get ticket statistics"""
        
        open_tickets = self._load_tickets(self.open_tickets_file)
        resolved_tickets = self._load_tickets(self.resolved_tickets_file)
        
        stats = {
            'total_open': len(open_tickets),
            'total_resolved': len(resolved_tickets),
            'by_priority': {},
            'by_category': {},
            'avg_resolution_time_hours': None
        }
        
        # Count by priority
        for ticket in open_tickets:
            priority = ticket['priority']
            stats['by_priority'][priority] = stats['by_priority'].get(priority, 0) + 1
        
        # Count by category
        for ticket in open_tickets:
            category = ticket['category']
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
        
        # Calculate average resolution time
        if resolved_tickets:
            resolution_times = []
            for ticket in resolved_tickets:
                if ticket['resolved_at']:
                    created = datetime.fromisoformat(ticket['timestamp'])
                    resolved = datetime.fromisoformat(ticket['resolved_at'])
                    diff_hours = (resolved - created).total_seconds() / 3600
                    resolution_times.append(diff_hours)
            
            if resolution_times:
                stats['avg_resolution_time_hours'] = sum(resolution_times) / len(resolution_times)
        
        return stats
    
    def export_daily_summary(self, date: str = None) -> str:
        """Export daily summary for team handover"""
        
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        open_tickets = self.get_open_tickets()
        stats = self.get_ticket_stats()
        
        summary = f"""
📋 DAILY SUPPORT SUMMARY - {date}
{'='*50}

🎯 OVERVIEW
-----------
Open Tickets: {stats['total_open']}
Resolved Today: {stats['total_resolved']}

📊 BY PRIORITY
--------------
"""
        
        for priority, count in stats['by_priority'].items():
            summary += f"{priority.upper()}: {count}\n"
        
        summary += f"""
📁 TICKETS REQUIRING ATTENTION
-------------------------------
"""
        
        # List high priority tickets first
        high_priority = [t for t in open_tickets if t['priority'] in ['urgent', 'high']]
        
        for ticket in high_priority:
            summary += f"""
🔴 [{ticket['priority'].upper()}] {ticket['ticket_id']}
   Customer: {ticket['customer_phone']}
   Issue: {ticket['question'][:100]}...
   Action: {ticket['suggested_action']}
"""
        
        summary += f"""
{'='*50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Save summary
        summary_file = os.path.join(self.storage_dir, f'daily_summary_{date}.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return summary


# Singleton instance
ticket_system = TicketSystem()


def create_ticket(**kwargs):
    """Convenience function to create a ticket"""
    return ticket_system.create_ticket(**kwargs)


def get_open_tickets(**kwargs):
    """Convenience function to get open tickets"""
    return ticket_system.get_open_tickets(**kwargs)


def get_ticket_stats():
    """Convenience function to get stats"""
    return ticket_system.get_ticket_stats()


if __name__ == '__main__':
    # Test ticket system
    ts = TicketSystem()
    
    # Create test ticket
    test_ticket = ts.create_ticket(
        customer_phone='+31612345678',
        question='Ik wil mijn product retourneren maar het lukt niet op de website',
        sentiment={'sentiment': 'negative', 'priority': 'high', 'score': -2},
        conversation_history=['Hallo', 'Ik wil retourneren', 'Het lukt niet'],
        reason='negative_sentiment',
        category='returns'
    )
    
    print(f"Created ticket: {test_ticket['ticket_id']}")
    print(f"Priority: {test_ticket['priority']}")
    print(f"Suggested action: {test_ticket['suggested_action']}")
    
    # Get stats
    stats = ts.get_ticket_stats()
    print(f"\nStats: {stats}")
    
    # Export summary
    summary = ts.export_daily_summary()
    print(f"\n{summary}")
