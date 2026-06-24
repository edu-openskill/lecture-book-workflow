package com.metacoding.orchestrator.message;

public record DeliveryCreatedEvent(int orderId, int deliveryId, boolean isSuccess) {}
