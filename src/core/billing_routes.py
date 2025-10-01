"""
Billing and Payment Routes for VeroctaAI
Handles Stripe integration, checkout, webhooks, and subscription management
"""

import os
import json
import logging
from datetime import datetime
from flask import jsonify, request, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from .app import app
from .auth import get_current_user
from ..services.payment_service import payment_service

# Stripe configuration
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test_demo')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

@app.route('/api/billing/config', methods=['GET'])
def get_billing_config():
    """Get billing configuration including Stripe publishable key"""
    try:
        return jsonify({
            'success': True,
            'publishable_key': STRIPE_PUBLISHABLE_KEY,
            'plans': {
                'free': {
                    'name': 'Free Plan',
                    'price': 0,
                    'currency': 'USD',
                    'features': ['Up to 5 reports', 'Basic analytics', 'CSV upload']
                },
                'professional': {
                    'name': 'Professional Plan', 
                    'price': 29,
                    'price_id': 'price_professional',
                    'currency': 'USD',
                    'features': ['Unlimited reports', 'Advanced AI insights', 'PDF reports', 'Priority support']
                },
                'enterprise': {
                    'name': 'Enterprise Plan',
                    'price': 99,
                    'price_id': 'price_enterprise', 
                    'currency': 'USD',
                    'features': ['Everything in Professional', 'Custom integrations', 'Dedicated support', 'White-label options']
                }
            }
        })
    except Exception as e:
        logging.error(f"Error getting billing config: {str(e)}")
        return jsonify({'error': 'Failed to get billing configuration'}), 500

@app.route('/api/billing/create-checkout', methods=['POST'])
@jwt_required()
def create_checkout_session():
    """Create Stripe Checkout session for subscription"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        price_id = data.get('price_id')
        
        if not price_id:
            return jsonify({'error': 'Price ID required'}), 400

        # Create or get Stripe customer
        customer = payment_service.create_customer(
            email=user['email'],
            name=f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or user['email'],
            company=user.get('company', 'Default Company')
        )
        
        if not customer:
            return jsonify({'error': 'Failed to create customer'}), 500

        # For demo mode, return demo checkout session
        if not payment_service.stripe_enabled:
            return jsonify({
                'success': True,
                'demo_mode': True,
                'checkout_url': f"{FRONTEND_URL}/billing/success?session_id=demo_session_123",
                'session_id': 'demo_session_123'
            })

        # Create Stripe Checkout Session
        import stripe
        try:
            checkout_session = stripe.checkout.Session.create(
                customer=customer['id'],
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{FRONTEND_URL}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{FRONTEND_URL}/billing/cancel",
                metadata={
                    'user_id': str(user['id']),
                    'user_email': user['email']
                }
            )
            
            return jsonify({
                'success': True,
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id
            })
            
        except stripe.error.StripeError as e:
            logging.error(f"Stripe checkout error: {str(e)}")
            return jsonify({'error': 'Failed to create checkout session'}), 500

    except Exception as e:
        logging.error(f"Create checkout error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/billing/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    try:
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get('Stripe-Signature')
        
        if not payload or not sig_header:
            logging.error("Missing payload or signature header")
            return jsonify({'error': 'Missing required data'}), 400

        # Handle webhook
        success = payment_service.handle_webhook(payload, sig_header)
        
        if success:
            logging.info("Webhook processed successfully")
            return jsonify({'success': True})
        else:
            logging.error("Webhook processing failed")
            return jsonify({'error': 'Webhook processing failed'}), 400

    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return jsonify({'error': 'Webhook processing failed'}), 400

@app.route('/api/billing/customer-portal', methods=['POST'])
@jwt_required()
def create_customer_portal():
    """Create Stripe Customer Portal session"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # For demo mode, redirect to demo portal
        if not payment_service.stripe_enabled:
            return jsonify({
                'success': True,
                'demo_mode': True,
                'portal_url': f"{FRONTEND_URL}/billing/manage"
            })

        # Get customer ID (would normally be stored in database)
        customer_id = f"demo_customer_{user['email'].replace('@', '_')}"
        
        import stripe
        try:
            portal_session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=f"{FRONTEND_URL}/billing"
            )
            
            return jsonify({
                'success': True,
                'portal_url': portal_session.url
            })
            
        except stripe.error.StripeError as e:
            logging.error(f"Stripe portal error: {str(e)}")
            return jsonify({'error': 'Failed to create customer portal'}), 500

    except Exception as e:
        logging.error(f"Customer portal error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/billing/subscription', methods=['GET'])
@jwt_required()
def get_subscription_status():
    """Get current subscription status for user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # For demo mode, return demo subscription
        if not payment_service.stripe_enabled:
            return jsonify({
                'success': True,
                'subscription': {
                    'id': 'demo_sub_123',
                    'status': 'active',
                    'plan': 'Professional',
                    'current_period_start': datetime.now().isoformat(),
                    'current_period_end': datetime.now().isoformat(),
                    'cancel_at_period_end': False
                },
                'demo_mode': True
            })

        # In production, retrieve actual subscription from Stripe
        # For now, return demo data
        return jsonify({
            'success': True,
            'subscription': {
                'id': None,
                'status': 'inactive',
                'plan': 'Free',
                'current_period_start': None,
                'current_period_end': None,
                'cancel_at_period_end': False
            }
        })

    except Exception as e:
        logging.error(f"Get subscription error: {str(e)}")
        return jsonify({'error': 'Failed to get subscription status'}), 500

@app.route('/api/billing/cancel-subscription', methods=['POST'])
@jwt_required()
def cancel_subscription():
    """Cancel user's subscription"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        subscription_id = data.get('subscription_id')
        
        if not subscription_id:
            return jsonify({'error': 'Subscription ID required'}), 400

        # For demo mode, return success
        if not payment_service.stripe_enabled:
            return jsonify({
                'success': True,
                'message': 'Subscription cancelled successfully (demo mode)',
                'demo_mode': True
            })

        # Cancel subscription
        success = payment_service.cancel_subscription(subscription_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Subscription cancelled successfully'
            })
        else:
            return jsonify({'error': 'Failed to cancel subscription'}), 500

    except Exception as e:
        logging.error(f"Cancel subscription error: {str(e)}")
        return jsonify({'error': 'Failed to cancel subscription'}), 500

@app.route('/api/billing/usage', methods=['GET'])
@jwt_required()
def get_billing_usage():
    """Get current billing usage and limits"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # In a real implementation, you would get usage from database
        # For now, return demo usage data
        usage_data = {
            'reports_generated': 12,
            'reports_limit': 50,
            'data_processed_gb': 2.5,
            'data_limit_gb': 10.0,
            'ai_insights_used': 45,
            'ai_insights_limit': 100,
            'billing_period_start': '2024-01-01T00:00:00Z',
            'billing_period_end': '2024-02-01T00:00:00Z',
            'next_billing_date': '2024-02-01T00:00:00Z'
        }

        return jsonify({
            'success': True,
            'usage': usage_data
        })

    except Exception as e:
        logging.error(f"Get usage error: {str(e)}")
        return jsonify({'error': 'Failed to get usage data'}), 500

@app.route('/api/billing/invoices', methods=['GET'])
@jwt_required()
def get_billing_invoices():
    """Get billing invoices for user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # For demo mode, return demo invoices
        demo_invoices = [
            {
                'id': 'inv_demo_001',
                'date': '2024-01-01',
                'amount': 29.00,
                'currency': 'USD',
                'status': 'paid',
                'pdf_url': '/api/billing/invoice/inv_demo_001/pdf'
            },
            {
                'id': 'inv_demo_002', 
                'date': '2023-12-01',
                'amount': 29.00,
                'currency': 'USD',
                'status': 'paid',
                'pdf_url': '/api/billing/invoice/inv_demo_002/pdf'
            }
        ]

        return jsonify({
            'success': True,
            'invoices': demo_invoices,
            'demo_mode': not payment_service.stripe_enabled
        })

    except Exception as e:
        logging.error(f"Get invoices error: {str(e)}")
        return jsonify({'error': 'Failed to get invoices'}), 500

# Add route to test payment flow
@app.route('/api/billing/test-payment', methods=['POST'])
@jwt_required()
def test_payment_flow():
    """Test payment flow for development"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Simulate successful payment
        test_data = {
            'customer_id': f"test_cus_{user['id']}",
            'subscription_id': f"test_sub_{user['id']}",
            'payment_intent_id': f"test_pi_{int(datetime.now().timestamp())}",
            'amount': 2900,  # $29.00
            'currency': 'usd',
            'status': 'succeeded'
        }

        return jsonify({
            'success': True,
            'message': 'Test payment processed successfully',
            'test_data': test_data
        })

    except Exception as e:
        logging.error(f"Test payment error: {str(e)}")
        return jsonify({'error': 'Test payment failed'}), 500