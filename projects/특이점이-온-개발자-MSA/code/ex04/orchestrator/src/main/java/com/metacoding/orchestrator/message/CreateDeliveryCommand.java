package com.metacoding.orchestrator.message;

public record CreateDeliveryCommand(int orderId, String address) {}
